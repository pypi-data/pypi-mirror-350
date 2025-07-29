from setuptools import setup, find_packages

setup(
    name="flagbox-sdk",
    version="0.0.2",
    description="FlagBox SDK for Python",
    author="FlagBox",
    author_email="support@flagbox.io",
    url="https://flagbox.io",
    packages=find_packages(),
    install_requires=[
        "requests>=2.25.0",
        "aiohttp>=3.8.0"
    ],
    python_requires=">=3.7",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    keywords=["FlagBox", "SDK"],
    project_urls={
        "Homepage": "https://flagbox.io",
    },
)