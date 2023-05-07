from flask import Response, jsonify, request
from dotenv import load_dotenv
import os

load_dotenv()


def middleware(next_app):
    def wrapper(environ, start_response):
        token = environ.get('HTTP_AUTHORIZATION')

        if not token:
            response = Response('Unauthorized', status=401)
            return response(environ, start_response)

        if (token.startswith('Bearer ')):
            token = token.replace('Bearer ', '')

        if token != os.environ.get('SECRET_KEY'):
            response = Response('Unauthorized', status=401)
            return response(environ, start_response)

        return next_app(environ, start_response)
    return wrapper
