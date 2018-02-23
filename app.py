#!/usr/bin/env python3
#-*- coding: utf-8 -*-
#TODO: Copy content from how to make a module
#from https://github.com/tomkralidis/pygeoapi
"""Entrance module starting flask for the bridge API,
apidocs follow http://127.0.0.1:5001/api/v1.0/apidocs"""

import os

import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, Blueprint
from flask_restful import Api
from flasgger import Swagger


from resources.v1.welcome import Welcome
from resources.v1.query import Query 
from resources.v1.upload import Upload
from resources.v1.tasks import Tasks


from resources.database.models import dbase

APP = Flask(__name__)
BLUEPRINT = Blueprint('tree', __name__)
PREFIX = "/api/v1.0"
API10 = Api(BLUEPRINT, prefix=PREFIX)


#Routes
API10.add_resource(Welcome, '/welcome')
API10.add_resource(Query, '/query')
API10.add_resource(Upload, '/upload')
API10.add_resource(Tasks, '/tasks/<uuid>')

#Blueprint Registration
APP.register_blueprint(BLUEPRINT)

#hack  this needs to be associeted with a specific version
Swagger.DEFAULT_CONFIG["static_url_path"] = os.path.join(
    PREFIX, "flasgger_static")
Swagger.DEFAULT_CONFIG["specs_route"] = os.path.join(
    PREFIX, "apidocs")
Swagger.DEFAULT_CONFIG["specs"][0]["route"] = os.path.join(
    PREFIX, "apispec_1.json")

Swagger(APP)

def do_database():
    """Checks if database exists and sets it up"""
    APP.logger.info("Initializing db")

    dbase.init_app(APP)
    if not os.path.isfile(APP.config["DBPATH"]):
        with APP.app_context():
            APP.logger.info("Creating new DB db.create_all()")
            dbase.create_all()


def do_logger():
    """Logger structure"""

    formater = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler(
        APP.config["LOG_FILE"], maxBytes=10000000, backupCount=5)
    handler.setFormatter(formater)
    handler.setLevel(logging.DEBUG)
    APP.logger.addHandler(handler)
    APP.logger.info("Logger operational")


if __name__ == '__main__':

    from etc import DevelopmentConfig as Config
    APP.config.from_object(Config)
    do_logger()
    do_database()
    #Logger for debugging
    APP.logger.info("Logger in debug mode")
    APP.run(debug=APP.config["DEBUG"],
            host=APP.config["HOST"],
            port=APP.config["PORT"])

else:
    from etc import ProductionConfig as Config
    APP.config.from_object(Config)
