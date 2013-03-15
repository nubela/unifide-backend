#===============================================================================
# backend for unifide
#===============================================================================
from flask import Flask
from local_config import API_TO_REGISTER, LOG_FILE, SQL_URI, DEBUG
import api
from flask.ext.pymongo import PyMongo


def _app_init(app):
    init_app(app, mongo)

    if app.config['DEBUG']:
        from werkzeug.wsgi import SharedDataMiddleware
        import os


        app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
            '/': os.path.join(os.path.dirname(__file__), 'static')
        })

    if not app.debug:
        import logging
        from logging import FileHandler


        file_handler = FileHandler(LOG_FILE)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)


def init_app(app, db):
    """
    initializes the app on first run
    - registeres it with apis
    """
    for api_name in API_TO_REGISTER:
        __import__("unifide_backend.api." + api_name)
        getattr(api, api_name)._register_api(app)


app = Flask(__name__)
app.debug = DEBUG
app.config['MONGO_URI'] = SQL_URI
mongo = PyMongo(app)