# setup.py
from setuptools import setup, find_packages

setup(
    name="django-env-checker",
    version="0.2.0",
    author="Rick Verbon",
    author_email="rick89@gmail.com",
    description="A simple Django env var checker",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RickVerbon/django-env-checker",
    packages=find_packages(),
    python_requires=">=3.9",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "Operating System :: OS Independent",
    ],
)
