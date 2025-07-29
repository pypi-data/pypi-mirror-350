#!/usr/bin/env python

# ...

from distutils.core import setup
from setuptools import setup, Extension

setup(name='pydantic-settings-qpython',
      version='2.9.1',
      description="Settings management using Pydantic",
      author='The QPYPI Team',
      author_email='qpypi@qpython.org',
      url='https://pypi.org/project/pydantic-settings/',
      packages=['pydantic_settings',],
      package_data={
        'pydantic_settings':[
"__init__.py",
"exceptions.py",
"main.py",
"py.typed",
"sources/*",
"sources/providers/*",
"utils.py",
"version.py",

        ]
},
      long_description="""
Settings management using Pydantic, this is the new official home of Pydantic's BaseSettings.

This package was kindly donated to the Pydantic organisation by Daniel Daniels, see pydantic/pydantic#4492 for discussion.
""",
      license="OSI Approved :: MIT License",
      install_requires=[
        'pydantic-qpython',
        'python-dotenv>=0.21.0',
        'typing-inspection>=0.4.0',
],
      classifiers=[
      "Intended Audience :: Developers",
      "Intended Audience :: Education",
      "Intended Audience :: Information Technology",
      "Intended Audience :: End Users/Desktop",
      "License :: OSI Approved :: Apache Software License",
      "Operating System :: Android",
      "Programming Language :: Python",
      "Programming Language :: Python :: 3.12",
      "Topic :: Software Development",
      ]
     )
