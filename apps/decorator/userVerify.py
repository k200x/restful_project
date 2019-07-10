import logging
import functools

from flask import request,g,jsonify

from apps.public.token import Token




def token_verify(fun):

    @functools.wraps(fun)
    def wrapper( *args, **kwargs):
        mode = request.values.get("mode")


        data = {}
        return jsonify(data)

    return wrapper





