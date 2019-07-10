import functools

from flask import jsonify

def token_verify(fun):

    @functools.wraps(fun)
    def wrapper( *args, **kwargs):

        data = {}
        return jsonify(data)

    return wrapper





