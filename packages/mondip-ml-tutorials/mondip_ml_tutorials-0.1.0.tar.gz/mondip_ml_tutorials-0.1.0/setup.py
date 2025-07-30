#!/usr/bin/env python
"""Setup script for mondip-ml-tutorials package."""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open(os.path.join(this_directory, 'requirements.txt'), encoding='utf-8') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="mondip-ml-tutorials",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A comprehensive collection of machine learning tutorials using NumPy, Pandas, Matplotlib, and Scikit-learn",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mondip-ml-tutorials",
    project_urls={
        "Documentation": "https://github.com/yourusername/mondip-ml-tutorials/blob/main/README.md",
        "Bug Reports": "https://github.com/yourusername/mondip-ml-tutorials/issues",
        "Source Code": "https://github.com/yourusername/mondip-ml-tutorials",
    },
    packages=find_packages(exclude=["tests", "tests.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers", 
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Education",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8", 
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    keywords="machine learning, tutorials, numpy, pandas, matplotlib, scikit-learn, data science, education",
    python_requires=">=3.7",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "twine>=3.0",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=1.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "mondip-ml-tutorials=mondip_ml_tutorials.tutorials:mondip",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)