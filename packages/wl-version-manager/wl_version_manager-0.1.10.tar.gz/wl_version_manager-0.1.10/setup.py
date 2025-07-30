#!/usr/bin/env python3

from setuptools import setup, find_packages
from wl_version_manager import VersionManager

with open("README.md", "r") as fh:
    long_description = fh.read()

version = VersionManager.get_version()


setup(
    name="wl_version_manager",
    version=version,
    author="Chris Watkins",
    author_email="chris@watkinslabs.com",
    description="Simple semantic version management for Python projects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/watkinslabs/version_manager",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Software Distribution",
    ],
    python_requires=">=3.6",
    entry_points={
        'console_scripts': [
            'wl_version_manager=wl_version_manager.cli:main',
        ],
    },
    keywords="version, versioning, semantic, semver, build, packaging",
    project_urls={
        "Bug Tracker": "https://github.com/watkinslabs/version_manager/issues",
        "Documentation": "https://github.com/watkinslabs/version_manager",
        "Source Code": "https://github.com/watkinslabs/version_manager",
    },
    license="BSD 3-Clause License",
)