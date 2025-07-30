from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="splore-sdk",
    version="0.1.37",
    author="DilipCoder",
    author_email="dilips.ven@splore.com",
    description="Python SDK for Splore",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/splorehq/splore-sdk-py",
    project_urls={
        "Homepage": "https://github.com/splorehq/splore-sdk-py",
        "Documentation": "https://github.com/splorehq/splore-sdk-py",
        "Changelog": "https://github.com/splorehq/splore-sdk-py/blob/main/CHANGELOG.md",
        "Issues": "https://github.com/splorehq/splore-sdk-py/issues",
        "Releases": "https://github.com/splorehq/splore-sdk-py/releases",
    },
    packages=find_packages(),
    classifiers=[
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
    python_requires=">=3.7",
    install_requires=[
        "requests>=2.28.0",
        "pydantic>=1.10.8,<2.0.0",
        "markdown>=3.4.4",
        "tuspy>=1.1.0",
    ],
    extras_require={
        "test": ["pytest>=7.0.0,<8.0.0", "pytest-mock>=3.0.0", "flake8>=5.0.0"],
        "examples": ["boto3>=1.37.30", "python-dotenv>=1.0.0"],
    },
)
