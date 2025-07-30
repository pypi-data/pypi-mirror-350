from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nltk_tools",
    version="0.1.2",
    author="NageGowda from Karnataka",
    author_email="akkirat2016@gmail.com",
    description="NLTK transformation package with tokenization, POS tagging, and TF-IDF functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krishaga/nltk_tools",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)