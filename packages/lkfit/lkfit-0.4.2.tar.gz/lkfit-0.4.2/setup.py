import setuptools
import os
import os.path
import codecs

with open("README.md", "r") as fh:
    long_description = fh.read()

def read(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in read(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")

setuptools.setup(
    name="lkfit",
    version=get_version("lkfit/__init__.py"),
    author="Lukas Kontenis",
    author_email="dse.ssd@gmail.com",
    description="A Python library for fitting.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
          'numpy', 'matplotlib>=2.1.0', 'scipy>=1.5.4', 'lkcom>=0.5.0', 'lmfit', 'scikit-image>=0.22.0'
    ],
    python_requires='>=3.6'
)
