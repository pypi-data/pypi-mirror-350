"""
Setup configuration for the orama-utils package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="orama-utils",
    version="0.1.8",
    author="Orama Solutions",
    author_email="keti@oramasolutions.io",
    description="A collection of utility functions for data processing and feature engineering",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Orama-Solutions/utils",
    packages=find_packages(include=["orama_utils", "orama_utils.*"]),
    package_data={
        'orama_utils': ['holiday_db/*.csv'],
    },
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
    ],
    python_requires=">=3.7",
    install_requires=[
        "pandas>=1.0.0",
        "numpy>=1.19.0",
    ],
    extras_require={
        'dev': [
            'pytest>=6.0.0',
            'pytest-cov>=2.0.0',
            'black>=21.0.0',
            'isort>=5.0.0',
            'flake8>=3.9.0',
        ],
    },
) 