#!/usr/bin/env python3
"""
Setup script for Pointer Activity Monitoring Service
Created by: Prof. Shahab Anbarjafari from 3S Holding OÜ, Tartu Estonia
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="pointer-activity-monitoring",
    version="1.0.0",
    author="Prof. Shahab Anbarjafari",
    author_email="",
    description="A comprehensive pointer activity monitoring service with heatmap visualization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/3sholding/pointer-activity-monitoring",
    py_modules=["pointer_monitor"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: System :: Monitoring",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "pointer-monitor=pointer_monitor:main",
        ],
    },
    keywords="mouse tracking, pointer monitoring, heatmap, visualization, user behavior",
    project_urls={
        "Bug Reports": "https://github.com/3sholding/pointer-activity-monitoring/issues",
        "Source": "https://github.com/3sholding/pointer-activity-monitoring",
        "Documentation": "https://github.com/3sholding/pointer-activity-monitoring#readme",
    },
)
