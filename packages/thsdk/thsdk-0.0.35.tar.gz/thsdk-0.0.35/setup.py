import codecs
import os
from setuptools import setup

# these things are needed for the README.md show on pypi
here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '0.0.35'
DESCRIPTION = 'a python package for thsdk'
LONG_DESCRIPTION = 'a python package for thsdk'

requires = [
]

setup(
    name="thsdk",
    version=VERSION,
    author="zengbotao",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=["thsdk"],
    include_package_data=True,
    install_requires=requires,
    keywords=['python', 'thsdk'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    package_data={
        'thsdk': ['*.so', '*.dll', '*.dylib', '*'],
    },
)
