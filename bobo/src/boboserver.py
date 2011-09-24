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
"""Create WSGI-based web applications.
"""

__all__ = (
    'Debug',
    'Reload',
    'server',
    'static',
    )

__metaclass__ = type

import bobo
import optparse
import os
import mimetypes
import pdb
import re
import sys
import traceback
import types
import webob

mimetypes.init()

def run_server(app, port):
    wsgiref.simple_server.make_server('', port, app).serve_forever()

if sys.version_info >= (2, 5):
    import wsgiref.simple_server
else:
    # can't use wsgiref, use paste
    import paste.httpserver

    def run_server(app, port):
        paste.httpserver.server_runner(app, {}, port=port)

class Directory:

    def __init__(self, root, path=None):
        self.root = os.path.abspath(root)+os.path.sep
        self.path = path or root

    @bobo.query('')
    def base(self, bobo_request):
        return bobo.redirect(bobo_request.url+'/')

    @bobo.query('/')
    def index(self):
        links = []
        for name in sorted(os.listdir(self.path)):
            if os.path.isdir(os.path.join(self.path, name)):
                name += '/'
            links.append('<a href="%s">%s</a>' % (name, name))
        return """<html>
        <head><title>%s</title></head>
        <body>
          %s
        </body>
        </html>
        """ % (self.path[len(self.root):], '<br>\n          '.join(links))

    @bobo.subroute('/:name')
    def traverse(self, request, name):
        path = os.path.abspath(os.path.join(self.path, name))
        if not path.startswith(self.root):
            raise bobo.NotFound
        if os.path.isdir(path):
            return Directory(self.root, path)
        else:
            return File(path)

bobo.scan_class(Directory)

class File:
    def __init__(self, path):
        self.path = path

    @bobo.query('')
    def base(self, bobo_request):
        response = webob.Response()
        content_type = mimetypes.guess_type(self.path)[0]
        if content_type is not None:
            response.content_type = content_type
        try:
            response.body = open(self.path, 'rb').read()
        except IOError:
            raise bobo.NotFound

        return response

bobo.scan_class(File)

def static(route, directory):
    """Create a resource that serves static files from a directory
    """
    return bobo.preroute(route, Directory(directory))

class Reload:
    """Module-reload middleware

    This middleware can *only* be used with bobo applications.  It
    monitors a list of modules given by a ``modules`` keyword
    parameter and configuration option.  When a module changes, it
    reloads the module and reinitializes the bobo application.

    The Reload class implements the `Paste Deployment
    filter_app_factory protocol
    <http://pythonpaste.org/deploy/#paste-filter-app-factory>`_ and is
    exported as a ``paste.filter_app_factory`` entry point named ``reload``.
    """

    def __init__(self, app, default, modules):
        if not isinstance(app, bobo.Application):
            raise TypeError("Reload can only be used with bobo applications")
        self.app = app

        self.mtimes = mtimes = {}
        for name in modules.split():
            module = sys.modules[name]
            mtimes[name] = (module.__file__, os.stat(module.__file__).st_mtime)

    def __call__(self, environ, start_response):
        for name, (path, mtime) in self.mtimes.iteritems():
            if os.stat(path).st_mtime != mtime:
                print 'Reloading', name
                execfile(path, sys.modules[name].__dict__)
                self.app.__init__(self.app.config)
                self.mtimes[name] = path, os.stat(path).st_mtime

        return self.app(environ, start_response)

class Debug:
    """Post-mortem debugging middleware

    This middleware catches uncaught exceptions and runs the
    ``pdb.post_mortem`` debugging function, helping you to debug
    exceptions raised by your application.

    The Debug class implements the `Paste Deployment
    filter_app_factory protocol
    <http://pythonpaste.org/deploy/#paste-filter-app-factory>`_ and is
    exported as a ``paste.filter_app_factory`` entry point named ``debug``.
    """

    def __init__(self, app, default=None):
        self.app = app

    def __call__(self, environ, start_response):
        try:
            return self.app(environ, start_response)
        except:
            traceback.print_exception(*sys.exc_info())
            pdb.post_mortem(sys.exc_info()[2])
            raise

_mod_re = re.compile(
    "(^|>) *(\w[a-zA-Z_.]*)(:|$)"
    ).search

def server(args=None, Application=bobo.Application):
    """Bobo development server

    The server function implements the bobo development server.

    It is exported as a ``console_script`` entry point named ``bobo``.

    An alternate application can be passed in to run the server with a
    different application implementation as long as application passed
    in subclasses bobo.Application.
    """

    if args is None:
        import logging; logging.basicConfig()
        args = sys.argv[1:]

    usage = "%prog [options] name=value ..."
    if sys.version_info >= (2, 5):
        usage = 'Usage: ' + usage
    parser = optparse.OptionParser(usage)
    parser.add_option(
        '--port', '-p', type='int', dest='port', default=8080,
        help="Specify the port to listen on.")
    parser.add_option(
        '--file', '-f', dest='file', action='append',
        help="Specify a source file to publish.")
    parser.add_option(
        '--resource', '-r', dest='resource', action='append',
        help=("Specify a resource, such as a module or module global,"
              " to publish."))
    parser.add_option(
        '--debug', '-D', action='store_true', dest='debug',
        help="Run the post mortem debugger for uncaught exceptions.")
    parser.add_option(
        '-c', '--configure', dest='configure',
        help="Specify the bobo_configure option.")
    parser.add_option(
        '-s', '--static', dest='static', action='append',
        help=("Specify a route and directory (route=directory)"
              " to serve statically"))

    def error(message):
        sys.stderr.write("Error:\n%s\n\n" % message)
        parser.parse_args(['-h'])

    options, pos = parser.parse_args(args)

    resources = options.resource or []
    mname = 'bobo__main__'
    for path in options.file or ():
        module = types.ModuleType(mname)
        module.__file__ = path
        execfile(module.__file__, module.__dict__)
        sys.modules[module.__name__] = module
        resources.append(module.__name__)
        mname += '_'

    for s in options.static or ():
        route, path = s.split('=', 1)
        resources.append("boboserver:static(%r,%r)" % (route, path))

    if not resources:
        error("No resources were specified.")

    if [a for a in pos if '=' not in a]:
        error("Positional arguments must be of the form name=value.")
    app_options = dict(a.split('=', 1) for a in pos)

    module_names = [m.group(2)
                    for m in map(_mod_re, resources)
                    if m is not None]

    if options.configure:
        if (':' not in options.configure) and module_names:
            options.configure = module_names[0]+':'+options.configure
        app_options['bobo_configure'] = options.configure

    app = Application(app_options, bobo_resources='\n'.join(resources))
    app = Reload(app, None, ' '.join(module_names))
    if options.debug:
        app = Debug(app)

    print "Serving %s on port %s..." % (resources, options.port)
    run_server(app, options.port)
