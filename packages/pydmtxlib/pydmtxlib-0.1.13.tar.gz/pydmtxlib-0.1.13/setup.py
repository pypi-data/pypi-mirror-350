#!/usr/bin/env python
import sys

import pydmtx

SCRIPTS = ["read_datamatrix", "write_datamatrix"]

# Optional dependency
PILLOW = "Pillow>=3.2.0"

URL = "https://github.com/pylibhub/pydmtx"


def readme():
    """Return the contents of the README file."""
    try:
        with open("README.rst", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return f"Visit {URL} for more details."


setup_data = {
    "name": "pydmtxlib",
    "version": pydmtx.__version__,
    "author": "pylibhub",
    "author_email": "pylibhub@gmail.com",
    "url": URL,
    "license": "MIT",
    "description": pydmtx.__doc__,
    "long_description": readme(),
    "long_description_content_type": "text/x-rst",
    "packages": ["pydmtx", "pydmtx.scripts", "pydmtx.tests"],
    "test_suite": "pydmtx.tests",
    "scripts": [f"pydmtx/scripts/{script}.py" for script in SCRIPTS],
    "entry_points": {
        "console_scripts": [
            f"{script}=pydmtx.scripts.{script}:main" for script in SCRIPTS
        ],
    },
    "extras_require": {
        "scripts": [
            PILLOW,
        ],
    },
    "tests_require": [
        # TODO How to specify OpenCV? 'cv2>=2.4.8',
        "numpy>=1.8.2",
        PILLOW,
    ],
    "include_package_data": True,
    "classifiers": [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
    ],
}


def setuptools_setup() -> None:
    """Set up the package using setuptools."""
    from setuptools import setup  # type: ignore[import]

    setup(**setup_data)


if (3, 8) <= sys.version_info:
    setuptools_setup()
else:
    sys.exit("Python versions 3.8 and above are supported")
