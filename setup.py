from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the relevant file
with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(
        name="elapsedtimer",
        version="0.4",
        description="Elapsed timer and utilities",
        long_description=long_description,
        author="Chris Reed",
        author_email="flit@me.com",
        license="BSD 3-Clause",
        url="https://github.com/flit/elapsedtimer",
        py_modules = ["elapsedtimer"],
        classifiers = [
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD License",
            "Development Status :: 4 - Beta",
            "Programming Language :: Python",
            "Operating System :: OS Independent",
            "Topic :: Other/Nonlisted Topic",
            "Topic :: Software Development :: Libraries",
            "Topic :: Software Development :: Libraries :: Python Modules",
        ]
    )
