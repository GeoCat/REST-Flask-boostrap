#!/usr/bin/python3
#-*- coding: utf-8 -*-
"""Module for testing query logins and returns the entered values"""
import os
from webargs.flaskparser import FlaskParser
from webargs import fields
from flasgger import swag_from
from flask_restful import Resource
from flask import jsonify
from flask import current_app as app
from flask import request
import marshmallow


class Upload(Resource):
    """Class with example on to upload a simple text filefile.
    Request max lenght could also be done with MAX_CONTENT_LENGTH"""

    mimetype = "text/plain"

    @swag_from("swagger/upload.yml")
    def post(self):
        """Uploads a file"""

        file_obj = FlaskParser.parse_files(self, request, "upfile", field=fields.Raw()) # pylint: disable=maybe-no-member

        if isinstance(file_obj, type(marshmallow.missing)): #werkzeug.datastructures.FileStorage
            return {"message":"File missing"}, 400 #Bad request

        size = Upload.get_size(file_obj)

        if size > app.config["MAX_UPLOAD"]:
            return {"message":"You exceded file limit of {}".format(app.config["MAX_UPLOAD"])}, 400

        if file_obj.mimetype != Upload.mimetype:
            return {"message":"File mimetype is {} instead of {}"
                              .format(str(file_obj.mimetype),
                                      Upload.mimetype)}, 415 #415 Unsupported Media Type

        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_obj.filename)
        file_obj.save(file_path)

        return jsonify(message="Saved file:{} with size {} bytes".format(file_path, size))

    @staticmethod
    def get_size(file_obj):
        """Gets the object sized of the file in memory"""
        file_obj.seek(0, os.SEEK_END)
        file_size = file_obj.tell()
        file_obj.seek(0)
        return file_size
