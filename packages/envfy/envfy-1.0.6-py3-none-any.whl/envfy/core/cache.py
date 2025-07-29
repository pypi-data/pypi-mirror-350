#!/usr/bin/env python3
"""
EnvFy Cache Management

Handles caching for performance optimization.
"""

import os
import json
import time
import hashlib
import pickle
from pathlib import Path
from typing import Any, Dict, List, Optional, Union, Callable
from dataclasses import dataclass, asdict
from threading import Lock

from .config import get_config
from ..utils.helpers import ensure_directory, get_file_hash
from ..utils.exceptions import EnvFyError


@dataclass
class CacheEntry:
    """Cache entry with metadata."""
    key: str
    value: Any
    created: float
    accessed: float
    hits: int = 0
    size: int = 0
    ttl: Optional[float] = None


class CacheManager:
    """Manages various caches for performance optimization."""
    
    def __init__(self):
        """Initialize cache manager."""
        self.config = get_config()
        self.cache_dir = self.config.cache_dir
        ensure_directory(self.cache_dir)
        
        # In-memory cache
        self._memory_cache: Dict[str, CacheEntry] = {}
        self._cache_lock = Lock()
        
        # Cache statistics
        self._stats = {
            'hits': 0,
            'misses': 0,
            'sets': 0,
            'deletes': 0,
            'clears': 0
        }
        
        # Initialize cache directories
        self._init_cache_dirs()
    
    def _init_cache_dirs(self) -> None:
        """Initialize cache directories."""
        cache_dirs = [
            'python_versions',
            'packages',
            'environments',
            'downloads',
            'metadata'
        ]
        
        for cache_dir in cache_dirs:
            ensure_directory(self.cache_dir / cache_dir)
    
    def _generate_key(self, namespace: str, *args, **kwargs) -> str:
        """Generate cache key from arguments."""
        key_data = {
            'namespace': namespace,
            'args': args,
            'kwargs': sorted(kwargs.items())
        }
        
        key_str = json.dumps(key_data, sort_keys=True)
        return hashlib.sha256(key_str.encode()).hexdigest()[:16]
    
    def _is_expired(self, entry: CacheEntry) -> bool:
        """Check if cache entry is expired."""
        if entry.ttl is None:
            # Use global TTL
            ttl = self.config.global_settings.cache_ttl
        else:
            ttl = entry.ttl
        
        if ttl <= 0:
            return False  # Never expires
        
        return (time.time() - entry.created) > ttl
    
    def get(self, namespace: str, *args, **kwargs) -> Optional[Any]:
        """
        Get value from cache.
        
        Args:
            namespace: Cache namespace
            *args: Cache key arguments
            **kwargs: Cache key keyword arguments
        
        Returns:
            Cached value or None if not found/expired
        """
        if not self.config.global_settings.cache_enabled:
            return None
        
        key = self._generate_key(namespace, *args, **kwargs)
        
        with self._cache_lock:
            entry = self._memory_cache.get(key)
            
            if entry is None:
                self._stats['misses'] += 1
                return None
            
            if self._is_expired(entry):
                del self._memory_cache[key]
                self._stats['misses'] += 1
                return None
            
            # Update access statistics
            entry.accessed = time.time()
            entry.hits += 1
            self._stats['hits'] += 1
            
            return entry.value
    
    def set(self, namespace: str, value: Any, ttl: Optional[float] = None, 
           *args, **kwargs) -> None:
        """
        Set value in cache.
        
        Args:
            namespace: Cache namespace
            value: Value to cache
            ttl: Time to live in seconds (optional)
            *args: Cache key arguments
            **kwargs: Cache key keyword arguments
        """
        if not self.config.global_settings.cache_enabled:
            return
        
        key = self._generate_key(namespace, *args, **kwargs)
        
        # Calculate size estimate
        try:
            size = len(pickle.dumps(value))
        except Exception:
            size = 0
        
        entry = CacheEntry(
            key=key,
            value=value,
            created=time.time(),
            accessed=time.time(),
            ttl=ttl,
            size=size
        )
        
        with self._cache_lock:
            self._memory_cache[key] = entry
            self._stats['sets'] += 1
            
            # Check cache size limits
            self._evict_if_needed()
    
    def delete(self, namespace: str, *args, **kwargs) -> bool:
        """
        Delete value from cache.
        
        Args:
            namespace: Cache namespace
            *args: Cache key arguments
            **kwargs: Cache key keyword arguments
        
        Returns:
            True if value was deleted
        """
        key = self._generate_key(namespace, *args, **kwargs)
        
        with self._cache_lock:
            if key in self._memory_cache:
                del self._memory_cache[key]
                self._stats['deletes'] += 1
                return True
            return False
    
    def clear(self, namespace: Optional[str] = None) -> None:
        """
        Clear cache entries.
        
        Args:
            namespace: Optional namespace to clear (all if None)
        """
        with self._cache_lock:
            if namespace is None:
                self._memory_cache.clear()
            else:
                # Clear entries matching namespace
                keys_to_delete = []
                for key, entry in self._memory_cache.items():
                    if entry.key.startswith(namespace):
                        keys_to_delete.append(key)
                
                for key in keys_to_delete:
                    del self._memory_cache[key]
            
            self._stats['clears'] += 1
    
    def _evict_if_needed(self) -> None:
        """Evict cache entries if size limits are exceeded."""
        max_entries = 1000  # Configurable limit
        
        if len(self._memory_cache) > max_entries:
            # Remove least recently accessed entries
            entries_by_access = sorted(
                self._memory_cache.items(),
                key=lambda x: x[1].accessed
            )
            
            # Remove oldest 10%
            to_remove = len(entries_by_access) // 10
            for key, _ in entries_by_access[:to_remove]:
                del self._memory_cache[key]
    
    def cached(self, namespace: str, ttl: Optional[float] = None):
        """
        Decorator for caching function results.
        
        Args:
            namespace: Cache namespace
            ttl: Time to live in seconds
        
        Returns:
            Decorator function
        """
        def decorator(func: Callable) -> Callable:
            def wrapper(*args, **kwargs):
                # Try to get from cache first
                cached_value = self.get(namespace, *args, **kwargs)
                if cached_value is not None:
                    return cached_value
                
                # Execute function and cache result
                result = func(*args, **kwargs)
                self.set(namespace, result, ttl, *args, **kwargs)
                return result
            
            return wrapper
        return decorator
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self._cache_lock:
            total_requests = self._stats['hits'] + self._stats['misses']
            hit_rate = (self._stats['hits'] / total_requests * 100) if total_requests > 0 else 0
            
            total_size = sum(entry.size for entry in self._memory_cache.values())
            
            return {
                'enabled': self.config.global_settings.cache_enabled,
                'entries': len(self._memory_cache),
                'total_size': total_size,
                'hits': self._stats['hits'],
                'misses': self._stats['misses'],
                'hit_rate': hit_rate,
                'sets': self._stats['sets'],
                'deletes': self._stats['deletes'],
                'clears': self._stats['clears']
            }
    
    def cache_python_versions(self, versions: List[Dict[str, str]]) -> None:
        """Cache Python version information."""
        self.set('python_versions', versions, ttl=3600)  # 1 hour
    
    def get_cached_python_versions(self) -> Optional[List[Dict[str, str]]]:
        """Get cached Python version information."""
        return self.get('python_versions')
    
    def cache_package_info(self, env_name: str, packages: List[Dict[str, str]]) -> None:
        """Cache package information for an environment."""
        self.set('packages', packages, ttl=300, env_name=env_name)  # 5 minutes
    
    def get_cached_package_info(self, env_name: str) -> Optional[List[Dict[str, str]]]:
        """Get cached package information for an environment."""
        return self.get('packages', env_name=env_name)
    
    def cache_environment_info(self, env_name: str, info: Dict[str, Any]) -> None:
        """Cache environment information."""
        self.set('environment_info', info, ttl=300, env_name=env_name)  # 5 minutes
    
    def get_cached_environment_info(self, env_name: str) -> Optional[Dict[str, Any]]:
        """Get cached environment information."""
        return self.get('environment_info', env_name=env_name)
    
    def cache_download(self, url: str, content: bytes) -> Path:
        """
        Cache downloaded content.
        
        Args:
            url: Download URL
            content: Downloaded content
        
        Returns:
            Path to cached file
        """
        # Generate filename from URL hash
        url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
        cache_file = self.cache_dir / 'downloads' / f"{url_hash}.cache"
        
        ensure_directory(cache_file.parent)
        
        with open(cache_file, 'wb') as f:
            f.write(content)
        
        # Store metadata
        metadata = {
            'url': url,
            'cached': time.time(),
            'size': len(content)
        }
        
        metadata_file = cache_file.with_suffix('.meta')
        with open(metadata_file, 'w') as f:
            json.dump(metadata, f)
        
        return cache_file
    
    def get_cached_download(self, url: str, max_age: float = 3600) -> Optional[bytes]:
        """
        Get cached download content.
        
        Args:
            url: Download URL
            max_age: Maximum age in seconds
        
        Returns:
            Cached content or None if not found/expired
        """
        url_hash = hashlib.sha256(url.encode()).hexdigest()[:16]
        cache_file = self.cache_dir / 'downloads' / f"{url_hash}.cache"
        metadata_file = cache_file.with_suffix('.meta')
        
        if not cache_file.exists() or not metadata_file.exists():
            return None
        
        # Check metadata
        try:
            with open(metadata_file, 'r') as f:
                metadata = json.load(f)
            
            # Check if expired
            if time.time() - metadata['cached'] > max_age:
                cache_file.unlink(missing_ok=True)
                metadata_file.unlink(missing_ok=True)
                return None
            
            # Read content
            with open(cache_file, 'rb') as f:
                return f.read()
                
        except Exception:
            # Clean up corrupted cache
            cache_file.unlink(missing_ok=True)
            metadata_file.unlink(missing_ok=True)
            return None
    
    def clean_downloads(self, max_age: float = 86400) -> int:
        """
        Clean old download cache files.
        
        Args:
            max_age: Maximum age in seconds (default: 24 hours)
        
        Returns:
            Number of files cleaned
        """
        downloads_dir = self.cache_dir / 'downloads'
        if not downloads_dir.exists():
            return 0
        
        cleaned = 0
        current_time = time.time()
        
        for cache_file in downloads_dir.glob('*.cache'):
            metadata_file = cache_file.with_suffix('.meta')
            
            try:
                if metadata_file.exists():
                    with open(metadata_file, 'r') as f:
                        metadata = json.load(f)
                    
                    if current_time - metadata['cached'] > max_age:
                        cache_file.unlink(missing_ok=True)
                        metadata_file.unlink(missing_ok=True)
                        cleaned += 1
                else:
                    # Remove cache files without metadata
                    cache_file.unlink(missing_ok=True)
                    cleaned += 1
                    
            except Exception:
                # Remove corrupted files
                cache_file.unlink(missing_ok=True)
                metadata_file.unlink(missing_ok=True)
                cleaned += 1
        
        return cleaned
    
    def clean_all(self) -> Dict[str, int]:
        """
        Clean all caches.
        
        Returns:
            Dictionary with cleanup statistics
        """
        stats = {
            'memory_entries': len(self._memory_cache),
            'downloads_cleaned': 0,
            'directories_cleaned': 0
        }
        
        # Clear memory cache
        self.clear()
        
        # Clean downloads
        stats['downloads_cleaned'] = self.clean_downloads()
        
        # Clean empty directories
        for cache_subdir in self.cache_dir.iterdir():
            if cache_subdir.is_dir():
                try:
                    if not any(cache_subdir.iterdir()):
                        cache_subdir.rmdir()
                        stats['directories_cleaned'] += 1
                except OSError:
                    pass
        
        return stats
    
    def get_cache_size(self) -> Dict[str, int]:
        """
        Get cache size information.
        
        Returns:
            Dictionary with size information
        """
        sizes = {
            'memory': sum(entry.size for entry in self._memory_cache.values()),
            'downloads': 0,
            'total_files': 0
        }
        
        # Calculate disk cache sizes
        for cache_file in self.cache_dir.rglob('*'):
            if cache_file.is_file():
                try:
                    file_size = cache_file.stat().st_size
                    sizes['total_files'] += 1
                    
                    if 'downloads' in str(cache_file):
                        sizes['downloads'] += file_size
                        
                except OSError:
                    pass
        
        return sizes
    
    def optimize(self) -> Dict[str, Any]:
        """
        Optimize cache performance.
        
        Returns:
            Optimization statistics
        """
        stats = {
            'entries_before': len(self._memory_cache),
            'entries_removed': 0,
            'downloads_cleaned': 0
        }
        
        with self._cache_lock:
            # Remove expired entries
            current_time = time.time()
            expired_keys = []
            
            for key, entry in self._memory_cache.items():
                if self._is_expired(entry):
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self._memory_cache[key]
                stats['entries_removed'] += 1
        
        # Clean old downloads
        stats['downloads_cleaned'] = self.clean_downloads()
        
        stats['entries_after'] = len(self._memory_cache)
        
        return stats


# Global cache instance
_cache_manager = None


def get_cache() -> CacheManager:
    """Get the global cache manager instance."""
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
    return _cache_manager 