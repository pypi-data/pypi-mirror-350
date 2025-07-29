from setuptools import setup, find_packages
import os


with open('README.md', 'r', encoding='utf-8') as f:
    description = f.read()

setup(
    name = "repcosn",
    version = "1.4.0",
    author = "Abhidnya Tambe",
    packages = find_packages(),
    install_requires = [
        #Nil
    ],

    long_description = description,
    long_description_content_type="text/markdown",
)