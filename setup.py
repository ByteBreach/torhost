#!/usr/bin/env python3

from setuptools import setup, find_packages
import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

version = "0.0.2"
init_path = os.path.join(BASE_DIR, "torhost", "__init__.py")
with open(init_path, "r") as f:
    for line in f:
        if line.startswith("__version__"):
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

with open(os.path.join(BASE_DIR, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="torhost",
    version=version,
    author="ByteBreach",
    author_email="mrfidal@proton.me",
    description="One-command setup for Tor hidden services (onion services)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bytebreach/torhost",

    packages=find_packages(exclude=("docs", "tests")),
    include_package_data=True,

    python_requires=">=3.6",

    entry_points={
        "console_scripts": [
            "torhost=torhost.cli:main",
        ],
    },

    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Security",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: System :: Networking",
    ],

    keywords="tor hidden-service onion privacy anonymity security",

    project_urls={
        "Bug Reports": "https://github.com/bytebreach/torhost/issues",
        "Source": "https://github.com/bytebreach/torhost",
        "Documentation": "https://torhost.readthedocs.io/",
    },

    license="MIT",
)
