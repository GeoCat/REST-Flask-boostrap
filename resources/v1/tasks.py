#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Creates a task in the database"""
# TODO: http://webargs.readthedocs.io/en/latest/advanced.html marshmallow integration
from flask_restful import Resource
from flask import jsonify
from resources.database.models import GenericTasks, dbase
from flasgger import swag_from
from resources.utils import is_valid_uuid
from webargs import fields
from webargs.flaskparser import use_kwargs
import sqlalchemy.exc


class Tasks(Resource):
    """Task creation (put) and get (get) of task. 
    Note that webargs already parses the json and return task as varible"""
    args = {
        'uuid': fields.String(
            required=True,
            validate=is_valid_uuid,
            location='view_args'
        )
    }

    json_args = {
        'task': fields.Str(
            required=True,
            location='json'
        )
    }

    @use_kwargs(args)
    @use_kwargs(json_args)
    @swag_from('swagger/task_put.yml')
    def put(self, **kwargs):
        """Creating a record with a specific uuid"""
        # {uuid': 'fe4a3e33-cb4b-42ac-b29b-a8160a85bf7e', 'task': 'I need to do homework'}
        uuid = kwargs.get("uuid")
        dbase.session.add(GenericTasks(**kwargs))
        try:
            dbase.session.commit()
            return {"message": "record inserted with uuid: {}".format(uuid)}, 201
        except sqlalchemy.exc.IntegrityError:
            return {"message": "DB integrity error maybe the UUID already exists, if so, DELETE it"}, 409

    @use_kwargs(args)
    @swag_from('swagger/task_delete.yml')
    def delete(self, uuid):
        """Delete the record"""
        record = GenericTasks.query.filter_by(uuid=uuid).first()
        if record:
            dbase.session.delete(record)
            dbase.session.commit()
            return {"message": "record  with uuid was deleted: {}".format(uuid)}, 200
        else:
            return {"message": "record  with uuid was not found: {}".format(uuid)}, 204

    @use_kwargs(args)
    @swag_from('swagger/task_get.yml')
    def get(self, uuid):
        record = dbase.session.query(GenericTasks).filter_by(uuid=uuid).first()
        if not record:
            return {"message": "record  with uuid {} NO FOUND".format(uuid)}, 404
        else:
            return jsonify(record.as_dict())
