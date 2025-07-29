from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="predictrampydata",
    version="0.1.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="Python client for Stock Data API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/predictrampydata",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)