"""A setuptools based setup module for ITUR-py."""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages

# To use a consistent encoding
from codecs import open as open_codecs
from os import path
import re

here = path.abspath(path.dirname(__file__))


def read_version():
    """
    Read __version__ from itur/__init__.py WITHOUT importing the package.

    Importing itur during setup triggers runtime imports (e.g., astropy) which
    fail under pip's isolated build environment.
    """
    version_file = path.join(here, "itur", "__version__.py")
    with open_codecs(version_file, "r", encoding="utf-8") as f:
        content = f.read()

    match = re.search(r"^__version__\s*=\s*['\"]([^'\"]+)['\"]", content, re.M)
    if not match:
        raise RuntimeError("Unable to find __version__ in itur/__version__.py")

    return match.group(1)


# Get the long description from the README file
with open_codecs(path.join(here, "README.rst")) as f:
    long_description = f.read()


setup(
    name="itur",
    version=read_version(),
    description="A python implementation of the ITU-R P. Recommendations",
    long_description=long_description,
    url="https://github.com/inigodelportillo/ITU-Rpy",
    author="Inigo del Portillo",
    author_email="inigo.del.portillo@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Telecommunications Industry",
        "Topic :: Scientific/Engineering :: Physics",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="atmopheric-propagation attenuation communications",
    packages=find_packages(exclude=["contrib", "docs", "tests"]),
    install_requires=["astropy", "scipy", "numpy", "pyproj"],
    package_data={
        "itur": [
            "LICENSE.txt",
            "README.md",
            "data/453/*.npz",
            "data/530/*.npz",
            "data/676/*.txt",
            "data/836/*.npz",
            "data/837/*.npz",
            "data/839/*.npz",
            "data/840/*.npz",
            "data/1510/*.npz",
            "data/1511/*.npz",
        ]
    },
    project_urls={
        "Bug Reports": "https://github.com/inigodelportillo/ITU-Rpy/issues",
        "Source": "https://github.com/inigodelportillo/ITU-Rpy/",
    },
)

