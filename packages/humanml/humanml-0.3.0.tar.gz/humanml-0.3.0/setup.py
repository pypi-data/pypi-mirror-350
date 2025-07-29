#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

setup(
    name="humanml",
    version="0.3.0",
    description="A user-friendly machine learning library with automated preprocessing, model selection, training, evaluation, and reinforcement learning capabilities",
    author="Rameez Anwar",
    author_email="rameezmughalrr@gmail.com",
    url="https://github.com/humanml/humanml",
    packages=find_packages(),
    install_requires=[
        "numpy>=1.19.0",
        "pandas>=1.0.0",
        "scikit-learn>=0.23.0",
        "matplotlib>=3.2.0",
        "seaborn>=0.10.0",
        "joblib>=0.15.0",
        "fpdf>=1.7.2",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.7",
)
