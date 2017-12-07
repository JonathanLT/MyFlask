import json
import functools
from flask import Flask
from flask import request

app = Flask(__name__)

GET = 'GET'
POST = 'POST'
PUT = 'PUT'
DELETE = 'DELETE'


def return_json(f):
    @functools.wraps(f)
    def inner(*a, **k):
        return json.dumps(f(*a, **k))
    return inner


@app.route('/', methods=[GET, POST])
def hello_world():
    return app.response_class(
        response=json.dumps('Hello GET!' if request.method == GET else 'Hello POST!'),
        status=200,
        mimetype='application/json'
    )


@app.route('/hello')
def hello():
    return app.response_class(
        response=json.dumps('Hello GET!' if request.method == GET else 'Hello POST!'),
        status=200,
        mimetype='application/json'
    )


@app.route('/', defaults={'path': ''}, methods=[GET, POST, PUT, DELETE])
@app.route('/<path:path>', methods=[GET, POST, PUT, DELETE])
def catch_all(path):
    return app.response_class(
        response=json.dumps('You want path: %s' % path),
        status=200,
        mimetype='application/json'
    )


@app.route('/test/<arg>')
@return_json
def test(arg):
    if arg == 'list':
        return [1, 2, 3]
    elif arg == 'dict':
        return {'a': 1, 'b': 2}
    elif arg == 'bool':
        return True
    return 'non of them'


if __name__ == '__main__':
    app.run()
