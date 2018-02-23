#!/usr/bin/python3
#-*- coding: utf-8 -*-
"""etc Module for classes defining Flask configuration.
PORT configuation and HOST are configured as arguments in app"""
from flask_env import MetaFlaskEnv
import os, tempfile

from __init__ import __version__

# pylint: disable=too-few-public-methods
class BaseConfig(metaclass=MetaFlaskEnv):
    """BaseClass from where other configurations will de derived"""
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False # Just to remove the warning and tracking of SQLALCHEMY 
    DBPATH= os.path.join(".", "task_database.db")
    SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(DBPATH)
    LOG_FILE = "flask.log"
    UPLOAD_FOLDER = tempfile.mkdtemp(prefix="rest_api") 
    PORT = 5001
    MAX_UPLOAD = 100
    VERSION = __version__
    HOST = "0.0.0.0"

# pylint: disable=too-few-public-methods
class DevelopmentConfig(BaseConfig):
    """Class with development configurations inhered from BaseConfig"""
    pass

# pylint: disable=too-few-public-methods
class ProductionConfig(BaseConfig):
    """Class with production configurations inhered from BaseConfig"""
    DEBUG = False
    