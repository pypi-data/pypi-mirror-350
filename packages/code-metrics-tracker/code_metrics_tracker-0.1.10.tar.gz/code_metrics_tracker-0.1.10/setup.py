#!/usr/bin/env python3
from setuptools import setup, find_packages
import os

# Read the long description from README.md
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="code-metrics-tracker",
    version="0.1.10",
    description="Code quality metrics tracking tool that combines Ruff, Radon, and cloc to generate detailed trends over time",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="AgileWorks",
    author_email="info@agileworks.co.za",
    url="https://github.com/AgileWorksZA/codeqa",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "codeqa": ["templates/*"],
    },
    entry_points={
        "console_scripts": [
            "codeqa=codeqa.cli:main",
        ],
    },
    python_requires=">=3.7",
    install_requires=[
        "setuptools>=42.0.0",
        "ruff>=0.0.254",
        "radon>=5.1.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Quality Assurance",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
    keywords="code quality metrics analysis static complexity maintainability linting ruff radon",
    project_urls={
        "Bug Tracker": "https://github.com/AgileWorksZA/codeqa/issues",
        "Documentation": "https://github.com/AgileWorksZA/codeqa/blob/main/README.md",
        "Source Code": "https://github.com/AgileWorksZA/codeqa",
    },
)