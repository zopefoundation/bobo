Bobo
====

Bobo is a light-weight framework for creating WSGI web applications.

Its goal is to be easy to use and remember.

It addresses 2 problems:

- Mapping URLs to objects

- Calling objects to generate HTTP responses

Bobo doesn't have a templating language, a database integration layer,
or a number of other features that are better provided by WSGI
middle-ware or application-specific libraries.

Bobo builds on other frameworks, most notably WSGI and WebOb.

To learn more. visit: http://bobo.digicool.com

Change History
==============

2.3.0 2014-11-21
----------------

- Bobo will encode Unicode URLs for redirects automatically.

2.2.0 2014-07-10
----------------

- Bobo will pass resource function arguments from data in JSON request bodies.

2.2.0 2014-07-10
----------------

- Bobo will now pass resource function arguments from data in JSON
  request bodies.

2.1.1 2014-07-06
----------------

- Fixed: Reloading modules sometimes failed

2.1.0 2014-04-06
----------------

- The ``bobo.Application`` constructor now accepts objects as well as
  strings for the bobo options. This makes application definition from
  Python a bit cleaner.

- A new ``bobo_handle_exceptions`` options makes it easy to tell bobo
  not to catch application exceptions.  This is helpful is you're
  using WSGI middleware to handle exceptions.

- The object provided to ``bobo_errors`` option can now provide a
  subset of error handlers.

2.0.0 2014-02-09
----------------

- Added Python 3 support!

- Add decorators to define resource handlers for additional HTTP methods
  (`put`, `get`, `head`, `delete`, `options`).

- With the addition of `bobo.put`, `bobo.post` was changed to no longer
  handle PUT requests.

1.0.0 2012-04-29
----------------

- Minimum supported Python version is 2.6.

- Updated to work with WebOb 1.2

- Added backtracking when searching for resources to deal with a case
  when a route doesn't handle a request method, but a later-matching
  route does.

- Bobo now catches application exceptions and generares 500 responses
  by default.

0.2.3 2012-03-12
----------------

Bugs fixed:

- Sanitize the request path included in the message on the default
  404 page.

0.2.2 2010-01-19
----------------

Bugs fixed:

- An intended optmization to cache resource decorator computations
  didn't work, making request handling slower than it should have
  been.

- URLs were sometimes treated as if they had extra slashes when
  traversing subroutes.

- boboserver.File must explicitly open files in binary mode, which is not
  the default on Windows.

0.2.1 2009-06-16
----------------

Packaging update to update documentation.

0.2.0 2009-05-26
----------------

Initial Public Release
