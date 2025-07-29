from setuptools import setup, find_packages
import os

setup(
    name = "pylumen",
    version = "v0.4", #will remove "v" soon, in official release -> 1.0
    packages = find_packages(include = ["lum", "lum.*"]),
    install_requires = [
        "requests",
        "pyperclip",
        "chardet",
        "tiktoken"
    ],
    entry_points = {
        "console_scripts": [
            "lum=lum.main:main",
        ],
    },
    author = "Far3k",
    author_email = "far3000yt@gmail.com",
    description = "Lumen: Intelligently prepares your codebase context for any LLM, solving context window limits with smart retrieval and providing deep project understanding.",
    long_description = open("README.md", encoding="utf-8").read() if os.path.exists("README.md") else "",    long_description_content_type = "text/markdown",
    url = "https://github.com/Far3000-YT/lumen",
    classifiers = [
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires = ">=3.7",
    license = "MIT",
)