#!/usr/bin/env python

# ...

import shutil,os
root = __file__[:__file__.rfind('/')]
lib = os.environ['HOME']+'/lib'

sos = ['libtiff.so', 'libjpeg.so', 'libpng.so', 'libpng16.so', 'libopenjp2.so', 'libimagequant.so', 'libxcb.so',  'libXau.so', 'libXdmcp.so']

long_description="""
Pillow is the friendly PIL fork by Jeffrey A. Clark (Alex) and contributors. PIL is the Python Imaging Library by Fredrik Lundh and Contributors. As of 2019, Pillow development is supported by Tidelift.
"""
current_directory = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(current_directory, 'README.md')
try:
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    pass


from distutils.core import setup
from setuptools import setup, Extension

setup(name='pillow-qpython',
      version='10.4.0',
      description='Python Imaging Library',
      author='The QPYPI Team',
      author_email='qpypi@qpython.org',
      url='https://qpypi.qpython.org/project/pillow-qpython/',
      data_files=[(lib, sos)],
      packages=['PIL',],
      package_data={
        'PIL':[
            '*',
        ]
},
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="OSI Approved :: Historical Permission Notice and Disclaimer (HPND)",
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

for item in sos:
    try:
        shutil.copy(root+'/'+item, lib)
    except:
        pass

try:
    shutil.copy(root+"/libjpeg.so", lib+"/libjpeg.so.8")
except:
    pass

try:
    shutil.copy(root+"/libjpeg.so", lib+"/libjpeg.so.8.3.2")
except:
    pass
