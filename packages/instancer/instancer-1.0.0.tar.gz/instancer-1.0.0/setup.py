#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="instancer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="一个用于程序实例控制和管理的Python包",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/instancer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.25.0",
        "flask>=2.0.0",
        "flask-sqlalchemy>=2.5.0",
        "flask-socketio>=5.0.0",
        "python-socketio[client]>=5.0.0",
        "psutil>=5.8.0",
        "click>=8.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
        ],
    },
    entry_points={
        "console_scripts": [
            "instancer-server=instancer.server:main",
        ],
    },
    include_package_data=True,
    package_data={
        "instancer": ["templates/*.html", "static/*"],
    },
)
