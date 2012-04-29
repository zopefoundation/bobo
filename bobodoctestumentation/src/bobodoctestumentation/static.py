import bobo, mimetypes, os, webob

@bobo.scan_class
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
        """ % (self.path[len(self.root):], '<br>\n  '.join(links))

    @bobo.subroute('/:name')
    def traverse(self, request, name):
        path = os.path.abspath(os.path.join(self.path, name))
        if not path.startswith(self.root):
            raise bobo.NotFound
        if os.path.isdir(path):
            return Directory(self.root, path)
        else:
            return File(path)

@bobo.scan_class
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
            response.body = open(self.path).read()
        except IOError:
            raise bobo.NotFound

        return response
