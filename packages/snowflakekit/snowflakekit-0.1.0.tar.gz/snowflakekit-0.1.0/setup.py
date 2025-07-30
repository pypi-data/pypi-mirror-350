from setuptools import setup, find_packages

setup(
    name="snowflakeid",
    version="0.1.0",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        # List your dependencies here
    ],
    author="Shudipto",
    description="Snowflake ID generation for asyncio",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/10XScale-in/snowflakeid",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    keywords="snowflake id generator asyncio",  # Add relevant keywords
)
