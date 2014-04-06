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
import manuel.capture
import manuel.codeblock
import manuel.doctest
import manuel.testing
import re
import six
import sys
import types
import unittest

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
        six.exec_(src, module.__dict__)

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
    options = (doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE |
               doctest.IGNORE_EXCEPTION_DETAIL)
    unicode_literal_normalizer = renormalizing.RENormalizing([
        (re.compile("u('.*?')"), r"\1"),
        (re.compile('u(".*?")'), r"\1"),
        ])
    suite = unittest.TestSuite((
        manuel.testing.TestSuite(
            manuel.doctest.Manuel(optionflags=options,
                                  checker=unicode_literal_normalizer) +
            manuel.capture.Manuel(),
            'index.txt', 'more.txt',
            setUp=setup_intro),
        doctest.DocFileSuite(
            'main.test', 'decorator.test',
            'fswiki.test', 'fswikia.test', 'bobocalc.test', 'static.test',
            optionflags=options,
            setUp=setUp, tearDown=setupstack.tearDown,
            checker=unicode_literal_normalizer),
        doctest.DocFileSuite(
            'boboserver.test',
            optionflags=options,
            setUp=setupstack.setUpDirectory, tearDown=setupstack.tearDown,
            checker=renormalizing.RENormalizing([
                (re.compile('usage:'), 'Usage:'),
                (re.compile('options:'), 'Options:'),
                ])
            ),
        ))
    if not six.PY2:
        suite.addTest(manuel.testing.TestSuite(
            manuel.doctest.Manuel() + manuel.codeblock.Manuel(),
            "annotations.test",
            setUp=setUp,
            tearDown=setupstack.tearDown))
    return suite
