#!/usr/bin/env python3
from setuptools import setup, find_packages
import os
with open(os.path.join("torhost", "__init__.py"), "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="torhost",
    version=version,
    author="ByteBreach",
    author_email="mrfidal@proton.me",
    description="A powerful tool to create Tor hidden services with one command",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bytebreach/torhost",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Networking",
    ],
    keywords="tor, hidden-service, onion, privacy, anonymity, security",
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "torhost=torhost.cli:main",
        ],
    },
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black>=21.0",
            "flake8>=3.9",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/bytebreach/torhost/issues",
        "Source": "https://github.com/bytebreach/torhost",
        "Documentation": "https://github.com/bytebreach/torhost/blob/main/README.md",
    },
    license="MIT",
)
