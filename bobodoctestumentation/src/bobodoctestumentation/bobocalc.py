import bobo, os

@bobo.query('/')
def html():
    return open(os.path.join(os.path.dirname(__file__),
                             'bobocalc.html')).read()

@bobo.query(content_type='application/json')
def add(value, input):
    value = int(value)+int(input)
    return dict(value=value)

@bobo.query(content_type='application/json')
def sub(value, input):
    value = int(value)-int(input)
    return dict(value=value)
