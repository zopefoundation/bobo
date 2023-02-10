##############################################################################
#
# Copyright Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################
from setuptools import setup


name = 'bobo'
version = '3.0.dev0'

entry_points = """
[console_scripts]
bobo = boboserver:server

[paste.app_factory]
main = bobo:Application

[paste.filter_app_factory]
reload = boboserver:Reload
debug = boboserver:Debug
"""


def read(fname):
    with open(fname) as f:
        return f.read()


setup(
    name=name,
    version=version,
    author="Jim Fulton",
    author_email="zope-dev@zope.dev",
    description="Web application framework for the impatient",
    license="ZPL 2.1",
    keywords=["WSGI", "microframework"],
    url='http://bobo.readthedocs.io',
    long_description=read('README.rst') + '\n\n' + read('CHANGES.rst'),
    py_modules=['bobo', 'boboserver'],
    package_dir={'': 'src'},
    python_requires='>=3.7',
    install_requires=["WebOb"],
    extras_require={
        'docs': ["Sphinx"],
    },
    entry_points=entry_points,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: Zope Public License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Server",
    ],
    zip_safe=False,
)
