#!/usr/bin/env python3
#
#  for development :
# pip3 install --use-pep517  -e . --upgrade  from virtual env.
#
import os
from setuptools import setup
#from fire import Fire

#-----------problematic------
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

import os.path

def readver(rel_path):
    here = os.path.abspath(os.path.dirname(__file__))
    with open(os.path.join(here, rel_path), 'r') as fp:
        return fp.read()

def get_version(rel_path):
    for line in readver(rel_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            version = line.split(delim)[1]
            print("i... setup.py: Version found:", version)  # Debug print
            return version
    else:
        raise RuntimeError("Unable to find version string.")

#if __name__ == "__main__":
#    print( get_version("cronvice/version.py")   )

setup(
    name="cronvice",
    description="Automatically created environment for python package",
    author="me",
    url="https://gitlab.com/ojr/cronvice",
    author_email="ojr@gmail.com",
    license="GPL2",
    version=get_version("cronvice/version.py"),
    packages=['cronvice'],
    package_data={"cronvice":["data/testik"]},
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    scripts = ['bin/cronvice'],
    install_requires = ['fire','console','sshkeyboard','pytermgui','blessings','terminaltables','pandas','pyfiglet','prompt_toolkit', 'python-crontab'],
)
