"""
Setup script for the polar-spark-df package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="polar-spark-df",
    version="0.1.0",
    author="amaye15",
    author_email="amaye15@github.com",
    description="High-performance converters between PySpark and Polars DataFrames",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amaye15/polar-spark-df",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Information Analysis",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "polars>=0.15.0",
        "pyspark>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-benchmark>=4.0.0",
            "numpy>=1.20.0",
            "psutil>=5.9.0",
        ],
    },
)