#!/usr/bin/env python3
"""
xPOURY4 Recon - Elite Cyber Intelligence & Digital Forensics Platform
Setup script for PyPI distribution
"""

from setuptools import setup, find_packages
import os
import re

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

# Get version from __init__.py
def get_version():
    with open("xPOURY4_recon/__init__.py", "r", encoding="utf-8") as fh:
        content = fh.read()
        version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", content, re.M)
        if version_match:
            return version_match.group(1)
        raise RuntimeError("Unable to find version string.")

# Package data
package_data = {
    'xPOURY4_recon.web': [
        'templates/*.html',
        'static/css/*.css',
        'static/js/*.js',
        'static/images/*'
    ]
}

setup(
    name="xPOURY4-recon",
    version=get_version(),
    author="xPOURY4",
    author_email="xpoury4@proton.me",
    description="Elite Cyber Intelligence & Digital Forensics Platform - Next-generation OSINT framework",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/xPOURY4/xPOURY4-recon",
    project_urls={
        "Bug Reports": "https://github.com/xPOURY4/xPOURY4-recon/issues",
        "Source": "https://github.com/xPOURY4/xPOURY4-recon",
        "Documentation": "https://github.com/xPOURY4/xPOURY4-recon#readme",
        "Changelog": "https://github.com/xPOURY4/xPOURY4-recon/releases",
    },
    packages=find_packages(exclude=["tests*", "docs*", "examples*", "Landingpage*"]),
    package_data=package_data,
    include_package_data=True,
    classifiers=[
        # Development Status
        "Development Status :: 4 - Beta",
        
        # Intended Audience
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        
        # Topic
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: System :: Networking :: Monitoring",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Information Analysis",
        
        # License
        "License :: OSI Approved :: MIT License",
        
        # Operating System
        "Operating System :: OS Independent",
        "Operating System :: POSIX :: Linux",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: MacOS",
        
        # Programming Language
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3 :: Only",
        
        # Environment
        "Environment :: Console",
        "Environment :: Web Environment",
        
        # Natural Language
        "Natural Language :: English",
    ],
    keywords=[
        "osint", "reconnaissance", "cybersecurity", "intelligence", "forensics",
        "github", "domain", "phone", "linkedin", "shodan", "security",
        "penetration-testing", "ethical-hacking", "digital-forensics",
        "threat-intelligence", "information-gathering", "recon", "investigation"
    ],
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=2.20.0",
        ],
        "web": [
            "flask>=2.3.0",
            "flask-socketio>=5.3.0",
            "gunicorn>=21.0.0",
        ],
        "all": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
            "mypy>=1.0.0",
            "pre-commit>=2.20.0",
            "flask>=2.3.0",
            "flask-socketio>=5.3.0",
            "gunicorn>=21.0.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "xpoury4-recon=xPOURY4_recon.main:main",
            "xpoury4=xPOURY4_recon.main:main",
        ],
    },
    zip_safe=False,
    platforms=["any"],
    license="MIT",
    
    # Additional metadata for PyPI
    maintainer="xPOURY4",
    maintainer_email="xpoury4@proton.me",
    
    # Security and compliance
    download_url="https://github.com/xPOURY4/xPOURY4-recon/archive/v1.0.1.tar.gz",
    
    # Package discovery
    package_dir={"": "."},
    
    # Data files
    data_files=[
        ("", ["LICENSE", "README.md", "requirements.txt", "config.yaml"]),
    ],
) 