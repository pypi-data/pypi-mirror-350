from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="tor-search",
    version="0.1.2",
    author="Anton Pavlenko",
    author_email="apavlenko@hmcorp.fund",
    description="Search the web anonymously through the Tor network",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/HMCorp-Fund/tor-search",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests",
        "beautifulsoup4",
        "pysocks",
    ],
    entry_points={
        "console_scripts": [
            "tor-search=tor_search.cli:main",
        ],
    },
)