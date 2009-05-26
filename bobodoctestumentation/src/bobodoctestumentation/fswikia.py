import bobo, os, webob

def config(config):
    global top
    top = config['directory']
    if not os.path.exists(top):
        os.mkdir(top)

edit_html = os.path.join(os.path.dirname(__file__), 'edit.html')

@bobo.query('/login.html')
def login(bobo_request, where=None):
    if bobo_request.remote_user:
        return bobo.redirect(where or bobo_request.relative_url('.'))
    return webob.Response(status=401)

@bobo.query('/logout.html')
def logout(bobo_request, where=None):
    response = bobo.redirect(where or bobo_request.relative_url('.'))
    response.delete_cookie('wiki')
    return response

def login_url(request):
    return request.application_url+'/login.html?where='+request.url

def logout_url(request):
    return request.application_url+'/logout.html?where='+request.url

def who(request):
    user = request.remote_user
    if user:
        return '''
        <div style="float:right">Hello: %s
        <a href="%s">log out</a></div>
        ''' % (user, logout_url(request))
    else:
        return '''
        <div style="float:right"><a href="%s">log in</a></div>
        ''' % login_url(request)

@bobo.query('/')
def index(bobo_request):
    return """<html><head><title>Bobo Wiki</title></head><body>
    <div style="float:left">Documents</div>%(who)s
    <hr style="clear:both" />
    %(docs)s
    </body></html>
    """ % dict(
        who=who(bobo_request),
        docs='<br />'.join('<a href="%s">%s</a>' % (name, name)
                           for name in sorted(os.listdir(top))),
        )

def authenticated(self, request, func):
    if not request.remote_user:
        return bobo.redirect(login_url(request))

@bobo.post('/:name', check=authenticated)
def save(bobo_request, name, body):
    open(os.path.join(top, name), 'w').write(body.encode('UTF-8'))
    return bobo.redirect(bobo_request.path_url, 303)

@bobo.query('/:name')
def get(bobo_request, name, edit=None):
    user = bobo_request.remote_user

    path = os.path.join(top, name)
    if os.path.exists(path):
        body = open(path).read().decode('UTF-8')
        if edit:
            return open(edit_html).read() % dict(
                name=name, body=body, action='Edit')

        if user:
            edit = ' (<a href="%s?edit=1">edit</a>)' % name
        else:
            edit = ''

        return '''<html><head><title>%(name)s</title></head><body>
        <div style="float:left">%(name)s%(edit)s</div>%(who)s
        <hr style="clear:both" />%(body)s</body></html>
        ''' % dict(name=name, body=body, edit=edit, who=who(bobo_request))

    if user:
        return open(edit_html).read() % dict(
            name=name, body='', action='Create')

    return '''<html><head><title>Not found: %(name)s</title></head><body>
        <h1>%(name)s doesn not exist.</h1>
        <a href="%(login)s">Log in</a> to create it.
        </body></html>
        ''' % dict(name=name, login=login_url(bobo_request))
