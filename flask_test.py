from flask import Flask, request
import logging
from functools import wraps
from flask_logging_decorator import flask_logging_decorator

app = Flask(__name__)
logger = logging.getLogger(__name__)

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s %(name)-14s %(levelname)s: %(message)s')

@flask_logging_decorator
def test():
    pass

@app.before_request
def before():
    app.logger.debug(f'request: {request.data.decode("utf-8")}')

# Useful debugging interceptor to log all endpoint responses
@app.after_request
def after(response):
    app.logger.warning(f'response: {response.data.decode("utf-8")}')
    return response

@app.route('/')
@flask_logging_decorator
def hello():
    test()
    return "Hello World!"

if __name__ == '__main__':
    app.run()
