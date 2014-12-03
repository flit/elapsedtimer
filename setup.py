from distutils.core import setup

long_description = """
Elapsed timer and utilities

Requires Python 2.7 or newer.
"""

setup(
        name="elapsedtimer",
        version="0.1",
        description="Elapsed timer and utilities",
        long_description=long_description,
        author="Chris Reed",
        author_email="flit@me.com",
        license="BSD 3-Clause",
        url="https://github.com/flit/elapsedtimer",
        py_modules = ["elapsedtimer"],
        classifiers = [
            "Intended Audience :: Developers",
            "License :: OSI Approved :: BSD 3-Clause License",
            "Development Status :: 4 - Beta",
            "Programming Language :: Python",
            "Operating System :: OS Independent",
            "Topic :: Other/Nonlisted Topic",
            "Topic :: Software Development :: Libraries",
        ]
    )
