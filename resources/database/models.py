#!/usr/bin/python3
#-*- coding: utf-8 -*-
"""Creates a task in the database"""
import datetime
import uuid
from flask_sqlalchemy import SQLAlchemy


dbase = SQLAlchemy()



#def toDict(self):
#    return { c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs }
class Serializer:
    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}



class GenericTasks(dbase.Model,Serializer):
    uuid = dbase.Column(dbase.String(), primary_key=True)
    task = dbase.Column(dbase.String(500), unique=False, nullable=False)
    timestamp = dbase.Column(dbase.DateTime(), default=datetime.datetime.now())