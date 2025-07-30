# setup.py

from setuptools import setup, find_packages

setup(
    name="dataclass_pprint_repr",
    version="0.1.2",
    author="Your Name",
    description="A decorator to enhance dataclass __repr__ formatting using pprint.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    url="https://github.com/ted-love/dataclass_pprint_repr",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # or whichever license you choose
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
