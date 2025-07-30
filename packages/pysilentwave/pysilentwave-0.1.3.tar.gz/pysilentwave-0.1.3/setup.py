from setuptools import setup, find_packages

setup(
    name="pysilentwave",
    version="0.1.3",
    description="API client for TheSilentWave devices",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="TheSilentWave",
    author_email="mail@thesilentwave.de",
    url="https://github.com/thesilentwave/pysilentwave",
    packages=find_packages(),
    install_requires=["aiohttp>=3.8.0"],
    python_requires=">=3.9",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)