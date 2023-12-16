from flask_restful import Api, Resource, reqparse
from apps import app
from flask_apispec import MethodResource, marshal_with, use_kwargs
from flask import Response, request
from marshmallow import fields
import http.client
import json
import traceback
import requests
from flask_swagger import swagger
from apps.committee.helpers import (
    CommitteeHelpers
)

api = Api(app)

class LoginApi(MethodResource):
    @use_kwargs({
        "username": fields.Str(),
        "password": fields.Str(),
    })
    def post(self, **kwargs):
        try:
            param = dict()
            param['api'] = "/api/v1/comitte/login"
            param['method'] = "POST"
            status, result = CommitteeHelpers(**param).authentication(kwargs)
            if (status == False):
                return Response(
                    json.dumps({
                        "success": False,
                        "message": "Failed to create the event",
                        "error": result
                    }),
                    mimetype='application/json'
                )
            return Response(
                json.dumps(
                    result
                ),
                mimetype='application/json'
            )
        except Exception as e:
            return Response(
                json.dumps(str(e)),
                status=http.client.INTERNAL_SERVER_ERROR,
                mimetype='application/json'
            )