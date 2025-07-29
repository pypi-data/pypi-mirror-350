from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="k-logging",
    version="1.0.0",
    author="june-oh",
    author_email="ohjs@sogang.ac.kr",
    description="Korean-friendly logging utility with abbreviated levels and Korean timezone",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/june-oh/k-logger",
    project_urls={
        "Bug Tracker": "https://github.com/june-oh/k-logger/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: System :: Logging",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "loguru>=0.6.0",
        "pytz>=2021.1",
    ],
    extras_require={
        "dev": [
            "pytest>=6.0",
            "black",
            "flake8",
            "mypy",
        ],
    },
    keywords="logging, korean, timezone, kst, loguru, abbreviated, simple",
) 