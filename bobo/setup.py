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
name = 'bobo'
version = '0'

long_description = """
Bobo is a light-weight framework for creating WSGI web applications.

It's goal is to be easy to use and remember. You don't have to be a genius.

It addresses 2 problems:

- Mapping URLs to objects

- Calling objects to generate HTTP responses

Bobo doesn't have a templateing language, a database integration layer,
or a number of other features that are better provided by WSGI
middle-ware or application-specific libraries.

Bobo builds on other frameworks, most notably WSGI and WebOb.

To learn more. visit: http://bobo.digicool.com
"""

entry_points = """
[console_scripts]
bobo = boboserver:server

[paste.app_factory]
main = bobo:Application

[paste.filter_app_factory]
reload = boboserver:Reload
debug = boboserver:Debug
"""

from ez_setup import use_setuptools
use_setuptools()
from setuptools import setup

import sys

if sys.version_info >= (2, 5):
    install_requires = ['WebOb']
else:
    install_requires = ['WebOb', 'PasteDeploy', 'Paste']

setup(
    name = name,
    version = version,
    author = "Jim Fulton",
    author_email = "jim@zope.com",
    description = "Web application framework for the impatient",
    license = "ZPL 2.1",
    keywords = "WSGI",
    url='http://www.python.org/pypi/'+name,
    long_description=long_description,

    py_modules = ['bobo', 'boboserver'],
    package_dir = {'':'src'},
    install_requires = install_requires,
    entry_points = entry_points,
    tests_require = ['bobodoctestumentation', 'webtest', 'zope.testing'],
    test_suite = 'bobodoctestumentation.tests.test_suite',
    )
