from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="nltktrans",
    version="0.1.0",
    author="NageGowda from Karnataka",
    author_email="akkirat2016@gmail.com",
    description="NLTK transformation package with tokenization, POS tagging, and TF-IDF functions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/krishaga/nltk_tools",
    packages=find_packages(),
    install_requires=[
        'nltk>=3.6',
        'pandas>=1.3',
        'numpy>=1.21',
        'scikit-learn>=1.0'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)