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
name = 'bobodoctestumentation'
version = '0'

long_description = """\
The bobo documentation and tests are broken out into a separate project
to keep the bobo distribution as small as possible.
"""

from setuptools import setup

setup(
    name = name,
    version = version,
    author = "Jim Fulton",
    author_email = "jim@zope.com",
    description = "Bobo tests and documentation",
    license = "ZPL 2.1",
    url='http://www.python.org/pypi/'+name,
    long_description=long_description,

    packages = ['bobodoctestumentation'],
    package_dir = {'':'src'},
    package_data = {'bobodoctestumentation': ['*.txt', '*.test', '*.html']},
    install_requires = ['manuel ==1.0.0a2', 'simplejson'],
    )
