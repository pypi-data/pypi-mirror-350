from setuptools import setup, find_packages

setup(
    name="Total5",
    version="0.1.0",
    description="Python client for Total.js platform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Peter Širka",
    author_email="petersirka@gmail.com",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
)
