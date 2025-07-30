import setuptools

import unittest
import os

version = os.getenv("HOUSES_SDK_VERSION", "0.1.0")

long_description = "HOUSES Client SDK"

setuptools.setup(
    name="houses-client",
    version=version,
    author="Tim Tschampel",
    author_email="tschampel.timothy@mayo.edu",
    description="HOUSES Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'oidc-client==0.2.6', 'requests==2.31.0'
    ],
    packages=setuptools.find_packages(exclude=["tests"]),
    python_requires=">=3.9",
)


