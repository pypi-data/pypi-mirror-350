from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.1'
DESCRIPTION = 'SUPERFACTORIAL'
LONG_DESCRIPTION = 'A package that simplifies the calculation of superfactorial of a number'

# Setting up
setup(
    name="Superfactorial",
    version=VERSION,
    author="Vaishnavi B",
    author_email="baratamvaishnavisklm@gmail.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=['math'],
    keywords=[],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)