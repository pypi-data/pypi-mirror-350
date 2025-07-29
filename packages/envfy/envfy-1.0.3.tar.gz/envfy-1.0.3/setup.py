#!/usr/bin/env python3
"""
EnvFy - Professional Virtual Environment Manager
A fast, precise, and user-friendly Python virtual environment management tool.
"""

from setuptools import setup, find_packages
import os
import codecs

here = os.path.abspath(os.path.dirname(__file__))

# Get the long description from the README file
def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r', encoding='utf-8') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

# Read README for long description
try:
    long_description = read("README.md")
except FileNotFoundError:
    long_description = "EnvFy - Professional Virtual Environment Manager"

setup(
    name="envfy",
    version=get_version("envfy/__init__.py"),
    author="EnvFy Development Team",
    author_email="support@envfy.dev",
    description="Fast, precise, and user-friendly Python virtual environment management",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/envfy/envfy",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Installation/Setup",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Environment :: Console",
    ],
    python_requires=">=3.7",
    install_requires=[
        "click>=8.0.0",
        "colorama>=0.4.4",
        "rich>=12.0.0",
        "virtualenv>=20.0.0",
        "packaging>=21.0",
        "psutil>=5.8.0",
        "requests>=2.25.0",
        "toml>=0.10.2",
        "pyyaml>=6.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0",
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
            "isort>=5.9.0",
            "pre-commit>=2.15.0",
        ],
        "docs": [
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
            "myst-parser>=0.15.0",
        ],
        "uv": [
            "uv>=0.1.0",  # Ultra-fast Python package installer
        ],
        "all": [
            "uv>=0.1.0",
            "pytest>=6.2.0",
            "pytest-cov>=2.12.0", 
            "black>=21.0.0",
            "flake8>=3.9.0",
            "mypy>=0.910",
            "isort>=5.9.0",
            "pre-commit>=2.15.0",
            "sphinx>=4.0.0",
            "sphinx-rtd-theme>=0.5.0",
            "myst-parser>=0.15.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "envfy=envfy.cli:main",
            "fy=envfy.cli:main",  # Short alias
        ],
    },
    include_package_data=True,
    package_data={
        "envfy": [
            "templates/*.txt",
            "templates/*.yml",
            "config/*.json",
        ],
    },
    keywords="virtual environment virtualenv venv python package management cli",
    project_urls={
        "Bug Reports": "https://github.com/envfy/envfy/issues",
        "Source": "https://github.com/envfy/envfy",
        "Documentation": "https://envfy.readthedocs.io/",
    },
) 