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
version = '0.0.0'

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
    long_description=open('README.txt').read(),

    py_modules = ['bobo', 'boboserver'],
    package_dir = {'':'src'},
    install_requires = install_requires,
    entry_points = entry_points,
    tests_require = [
        'bobodoctestumentation >=%s, <%s.999' % (version, version)],
    test_suite = 'bobodoctestumentation.tests.test_suite',
    )
