from setuptools import setup, find_packages
import os
import codecs

# Try to read README.md with UTF-8 encoding safely
try:
    with codecs.open("README.md", "r", "utf-8") as fh:
        long_description = fh.read()
except Exception:
    # Fallback to simple description if README.md cannot be read
    long_description = "TulgaTTS is an AI-based text-to-speech (TTS) library that generates speech using various voices popular in Kazakhstan. It leverages Character AI technology to synthesize natural-sounding speech from text."

setup(
    name="tulgatts",
    version="0.1.3",
    author="David Suragan",
    author_email="dauitsuragan002@gmail.com",
    description="Uses Character AI for synthesis.",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Use Markdown format
    url="https://github.com/dauitsuragan002/tulgatts",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "PyCharacterAI>=0.2.0",
        "requests>=2.20.0",
        "python-dotenv>=0.10.0",
    ],
    extras_require={
        "audio": ["pygame>=2.0.0"],
    },
    package_data={
        "tulgatts": ["py.typed"],
    },
) 