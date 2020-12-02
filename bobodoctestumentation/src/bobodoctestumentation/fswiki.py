import bobo, os

def config(config):
    global top
    top = config['directory']
    if not os.path.exists(top):
        os.mkdir(top)

edit_html = os.path.join(os.path.dirname(__file__), 'edit.html')

@bobo.query('/')
def index():
    return """<html><head><title>Bobo Wiki</title></head><body>
    Documents
    <hr />
    %(docs)s
    </body></html>
    """ % dict(
        docs='<br />'.join('<a href="%s">%s</a>' % (name, name)
                           for name in sorted(os.listdir(top)))
        )

@bobo.post('/:name')
def save(bobo_request, name, body):
    with open(os.path.join(top, name), 'w') as f:
        f.write(body)
    return bobo.redirect(bobo_request.path_url, 303)

@bobo.query('/:name')
def get(name, edit=None):
    path = os.path.join(top, name)
    if os.path.exists(path):
        with open(path) as f:
            body = f.read()
        if edit:
            with open(edit_html) as f:
                return f.read() % dict(
                    name=name, body=body, action='Edit')

        return '''<html><head><title>%(name)s</title></head><body>
        %(name)s (<a href="%(name)s?edit=1">edit</a>)
        <hr />%(body)s</body></html>
        ''' % dict(name=name, body=body)

    with open(edit_html) as f:
        return f.read() % dict(
            name=name, body='', action='Create')
