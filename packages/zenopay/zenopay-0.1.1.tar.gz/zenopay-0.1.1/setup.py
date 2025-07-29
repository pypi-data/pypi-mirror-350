"""Packaging."""

from pathlib import Path

from setuptools import find_packages, setup

with Path("README.md").open() as file:
    long_description = file.read()

setup(
    name="zenopay",
    version="0.1.1",
    description="A Python wrapper for ZenoPay Payment API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jovyinny/zenopay",
    author="Jovine Mutelani",
    author_email="jovinerobotics@gmail.com",
    packages=find_packages(exclude=["tests", "tests.*"]),
    license="MIT",
    keywords=[
        "zenopay",
        "zenopay SDK",
        "zeno pay SDK",
        "ZenoPay Wrapper",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/jovyinny/zenopay/issues",
        "Documentation": "https://jovyinny.github.io/zenopay/",
        "Source Code": "https://github.com/jovyinny/zenopay",
    },
    python_requires=">=3.7",
    install_requires=["requests", "phonenumbers"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
