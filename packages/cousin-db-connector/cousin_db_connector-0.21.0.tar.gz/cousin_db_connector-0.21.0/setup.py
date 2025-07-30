from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cousin_db_connector",
    version="0.21.0",
    author="Eduardo Ponce",
    description='is a Python library designed to simplify connecting to and managing '
                'databases in asynchronous and synchronous applications. '
                'It provides a unified interface for interacting '
                'with different database engines, starting '
                'with support for MongoDB and expanding to others in the future.',
    long_description=long_description,
    long_description_content_type="text/markdown",  # O "text/x-rst" si usas ReStructuredText
    packages=find_packages(),
    install_requires=[
        'PyJWT',
        'fastapi',
        'starlette',
        'setuptools',
        'motor',
        'pymongo',
        'twine',
        'pytest',
        'pytest-asyncio',
        'pydantic'
    ],
    python_requires='>=3.9',
)