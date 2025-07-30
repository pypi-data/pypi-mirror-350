#!/usr/bin/env python

# ...

from distutils.core import setup
from setuptools import setup, Extension
import shutil,os

root = __file__[:__file__.rfind('/')]
lib = os.environ['HOME']+'/lib'

sos = ['libxslt.so', 'libexslt.so']

current_directory = os.path.dirname(os.path.abspath(__file__))
readme_path = os.path.join(current_directory, 'README.md')
try:
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = """Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API"""

setup(name='lxml-qpython',
      version='5.3.0',
      description='Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API',
      author='The Lxml Development Team',
      author_email='support@qpython.org',
      data_files=[(lib, sos)],
      url='https://pypi.org/project/lxml/',
      packages=['lxml',],
      package_data={
        'lxml':[
"ElementInclude.py",
"__init__.py",
"_elementpath.cpython-312.so",
"_elementpath.py",
"apihelpers.pxi",
"builder.cpython-312.so",
"builder.py",
"classlookup.pxi",
"cleanup.pxi",
"cssselect.py",
"debug.pxi",
"docloader.pxi",
"doctestcompare.py",
"dtd.pxi",
"etree.cpython-312.so",
"etree.h",
"etree.pyx",
"etree_api.h",
"extensions.pxi",
"html/*",
"includes/*",
"isoschematron/*",
"isoschematron/resources/rng/*",
"isoschematron/resources/xsl/*",
"isoschematron/resources/xsl/iso-schematron-xslt1/*",
"iterparse.pxi",
"lxml.etree.h",
"lxml.etree_api.h",
"nsclasses.pxi",
"objectify.cpython-312.so",
"objectify.pyx",
"objectpath.pxi",
"parser.pxi",
"parsertarget.pxi",
"proxy.pxi",
"public-api.pxi",
"pyclasslookup.py",
"readonlytree.pxi",
"relaxng.pxi",
"sax.cpython-312.so",
"sax.py",
"saxparser.pxi",
"schematron.pxi",
"serializer.pxi",
"usedoctest.py",
"xinclude.pxi",
"xmlerror.pxi",
"xmlid.pxi",
"xmlschema.pxi",
"xpath.pxi",
"xslt.pxi",
"xsltext.pxi",

        ]
},
      long_description=long_description,
      long_description_content_type="text/markdown",
      license="MIT AND (Apache-2.0 OR BSD-2-Clause)",
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
],
     )

for item in sos:
    try:
        shutil.copy(root+'/'+item, lib)
    except:
        pass


