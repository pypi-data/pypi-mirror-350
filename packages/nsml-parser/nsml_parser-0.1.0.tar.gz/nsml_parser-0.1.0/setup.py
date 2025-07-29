from setuptools import setup, find_packages

setup(
    name="nsml-parser",
    version="0.1.0",
    author="catchmaurya(catchmaurya@gmail.com) and NeuroBujandar",
    author_email="catchmaurya@gmail.com",
    description="NSML++: Neuro-Symbolic Memory Lattice for Intelligent Log Parsing",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/catchmaurya/nsml-parser",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

