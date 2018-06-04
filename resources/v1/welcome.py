#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""Welcome message of REST api. This is for testing purpose only"""

import datetime
from flask import jsonify
from flask import current_app as app
from flask_restful import Resource
from flasgger import swag_from


class Welcome(Resource):
    """Welcome class for testing REST"""

    # pylint: disable=R0201
    @swag_from('swagger/welcome.yml')
    def get(self):
        """GET Request code"""
        now = datetime.datetime.now()

        app.logger.debug("Time of request {}".format(now))

        return jsonify({"message": "Lekker!!!", "version": app.config["VERSION"], "date": now})
