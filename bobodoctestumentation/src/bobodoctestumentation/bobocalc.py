import bobo, os

@bobo.query('/')
def html():
    with open(os.path.join(os.path.dirname(__file__), 'bobocalc.html')) as f:
        return f.read()

@bobo.query(content_type='application/json')
def add(value, input):
    value = int(value)+int(input)
    return dict(value=value)

@bobo.query(content_type='application/json')
def sub(value, input):
    value = int(value)-int(input)
    return dict(value=value)
