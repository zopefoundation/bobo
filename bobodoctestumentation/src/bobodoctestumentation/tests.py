##############################################################################
#
# Copyright (c) 2006 Zope Corporation and Contributors.
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.0 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#
##############################################################################

from zope.testing import doctest, setupstack, renormalizing
import bobo
import manuel
import manuel.doctest
import manuel.testing
import pprint
import re
import sys
import textwrap
import types
import unittest
import webob

def assignment_manuel():
    assignment_re = re.compile(
        r"[^\n]*::(?P<value>(\n| [^\n]*\n)+?)"
        " *\.\. -> (?P<name>\w+)(?P<strip> +strip)? *\n")

    m = manuel.Manuel()

    @m.parser
    def parse(document):
        for region in document.find_regions(assignment_re):
            data = region.start_match.groupdict()
            data['value'] = textwrap.dedent(data['value'].expandtabs())
            if data.get('strip'):
                data['value'] = data['value'].strip()
            source = "%(name)s = %(value)r\n" % data
            example = doctest.Example(source, '', lineno=region.lineno-1)
            document.replace_region(region, example)

    m2 = manuel.doctest.Manuel()
    m2.extend(m)

    return m2

def setUp(test):
    setupstack.setUpDirectory(test)

    for i in ('1', '2'):
        name = 'testmodule'+i
        module = types.ModuleType('bobo.'+name)
        setattr(bobo, name, module)
        sys.modules[module.__name__] = module
        setupstack.register(test, delattr, bobo, name)
        setupstack.register(test, sys.modules.__delitem__, module.__name__)

def setup_intro(test):
    setupstack.setUpDirectory(test)

    def update_module(name, src):
        if name not in sys.modules:
            sys.modules[name] = types.ModuleType(name)
            setupstack.register(test, sys.modules.__delitem__, name)
        module = sys.modules[name]
        exec src in module.__dict__

    test.globs['update_module'] = update_module


# XXX This should move to zope.testing
import random, socket
def get_port():
    """Return a port that is not in use.

    Checks if a port is in use by trying to connect to it.  Assumes it
    is not in use if connect raises an exception.

    Raises RuntimeError after 10 tries.
    """
    for i in range(10):
        port = random.randrange(20000, 30000)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            try:
                s.connect(('localhost', port))
            except socket.error:
                # Perhaps we should check value of error too.
                return port
        finally:
            s.close()
    raise RuntimeError("Can't find port")

def test_suite():
    return unittest.TestSuite((
        manuel.testing.TestSuite(
            assignment_manuel(),
            'index.txt', 'more.txt',
            setUp=setup_intro),
        doctest.DocFileSuite(
            'main.test', 'decorator.test',
            'fswiki.test', 'fswikia.test', 'bobocalc.test', 'static.test',
            setUp=setUp, tearDown=setupstack.tearDown),
        doctest.DocFileSuite(
            'boboserver.test',
            setUp=setupstack.setUpDirectory, tearDown=setupstack.tearDown,
            checker=renormalizing.RENormalizing([
                (re.compile('usage:'), 'Usage:'),
                (re.compile('options:'), 'Options:'),
                ])
            ),
        ))
