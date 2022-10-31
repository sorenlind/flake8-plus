"""Setup script for package."""
# pylint: disable=consider-using-with, no-self-use
import os
import re
import sys
from typing import Optional

from setuptools import Command, find_packages, setup

match = re.search(
    r'^VERSION\s*=\s*"(.*)"',
    open("flake8_plus/version.py", encoding="utf_8").read(),
    re.M,
)
VERSION = match.group(1) if match else "???"
with open("README.md", "rb") as f:
    LONG_DESCRIPTION = f.read().decode("utf-8")


class VerifyVersion(Command):
    """Command for verifying that git tag matches package version."""

    description = "verify that the git tag matches package version"
    user_options = []

    def initialize_options(self):
        """Implement required method for Command."""

    def finalize_options(self):
        """Implement required method for Command."""

    def run(self):
        """
        Check that the git tag matches the package version.

        If it doesn't match, exit.
        """
        tag = os.getenv("CIRCLE_TAG")
        if not _validate_version(tag, VERSION):
            info = f"Git tag: '{tag}' does not match package version: {VERSION}"
            sys.exit(info)


def _validate_version(tag: Optional[str], version: str) -> bool:
    if not tag:
        return version == "0.0.0"
    if tag[0] != "v":
        return False
    return tag[1:] == version


setup(
    name="flake8-plus",
    version=VERSION,
    description="Flake8 plugin adding PEP8-compliant vertical whitespacing rules",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Soren Kristiansen",
    author_email="sorenlind@mac.com",
    url="https://github.com/sorenlind/flake8-plus",
    keywords="",
    packages=find_packages(),
    install_requires=["flake8"],
    extras_require={
        "dev": [
            "astpretty",
            "bandit",
            "black",
            "coverage",
            "flake8",
            "flake8-annotations",
            "flake8-pytest-style",
            "mypy",
            "pycodestyle",
            "pydocstyle",
            "pylint",
            "rope",
            "pyenchant",
            "pytest",
            "pytest-cov",
            "pytest-mock",
            "tox",
        ],
        "test": [
            "coverage",
            "pytest",
            "pytest-cov",
            "pytest-mock",
            "tox",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
    ],
    cmdclass={
        "verify": VerifyVersion,
    },
    entry_points={
        "flake8.extension": [
            "PLU = flake8_plus:Plugin",
        ],
    },
)
