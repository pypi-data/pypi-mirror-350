from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="voyado-engage",
    version="0.1.0",
    author="Ali Shaheen",
    author_email="ali.shaheen@zenloop.com",
    description="A Python client library for Voyado Engage API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alinaqi/voyado-python",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
        "typing-extensions>=4.0.0",
        "python-dateutil>=2.8.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "black>=22.0.0",
            "flake8>=4.0.0",
            "mypy>=0.950",
            "python-dotenv>=0.20.0",
        ]
    }
)
