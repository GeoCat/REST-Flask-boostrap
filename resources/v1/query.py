#!/usr/bin/python3
#-*- coding: utf-8 -*-
"""Module for testing query logins and returns the entered values"""
from webargs.flaskparser import  use_kwargs
from webargs import fields
from flasgger import swag_from
from flask_restful import Resource
from flask import jsonify


class Query(Resource):
    """Query class testing 2 inputs one numerical other string"""
    args = {
        'number': fields.Float( #pylint: disable=E1101
            required=True,
            validate=lambda x: -1.0 <= x <= 1.0
        ),
        'string' : fields.Str( #pylint: disable=E1101
            required=False,
            validate=lambda x: x in ["dog", "cat"]
        )
    }
    @use_kwargs(args)
    @swag_from("swagger/query.yml")
    def get(self, number, string): #pylint: disable=R0201
        """Method returning input"""
        return jsonify(number=number, string=string)
        