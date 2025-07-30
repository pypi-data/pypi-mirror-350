#!/usr/bin/env python3
from setuptools import setup, find_packages

# Версия задается вручную
VERSION = "0.1.1"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="project-cleaner",
    version=VERSION,
    author="Flaymie",
    author_email="funquenop@gmail.com",
    description="Очистка проектов от временных файлов и папок",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Flaymie/project-cleaner",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Software Development :: Build Tools",
        "Topic :: Utilities",
    ],
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "project-cleaner=project_cleaner.cleaner:main",
        ],
    },
) 