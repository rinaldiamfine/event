from flask_restful import Api, Resource, reqparse
from apps import app
from flask_apispec import MethodResource, marshal_with, use_kwargs
from apps.event.helpers import (
    EventHelpers,
    EventRegistrationHelpers
)
from apps.event.schemas import (
    EventSchema,
    EventRegistrationSchema
)
from flask import Response, request
from marshmallow import fields
import http.client
import json
import traceback
import requests
from flask_swagger import swagger

api = Api(app)

class EventApi(MethodResource):
    @use_kwargs({
        "name": fields.Str(),
        "code": fields.Str(),
        "event_date": fields.DateTime()
    })
    @marshal_with(EventSchema)
    def post(self, **kwargs):
        try:
            param = dict()
            param['api'] = "/api/v1/events"
            param['method'] = "POST"
            status, result = EventHelpers(**param).create(kwargs)
            return result
        except Exception as e:
            return Response(
                json.dumps(str(e)),
                status=http.client.INTERNAL_SERVER_ERROR,
                mimetype='application/json'
            )
        
    def get(self, **kwargs):
        print(kwargs)
        params = request.args.to_dict()
        print(params)
        status, result =  EventHelpers().read(params)
        return result
    

class EventLineApi(MethodResource):
    def post(self, **kwargs):
        print("LALA", kwargs)


class EventRegistrationApi(MethodResource):
    @use_kwargs({
        "event_id": fields.Int(),
        "name": fields.Str(),
        "phone": fields.Str(),
        "email": fields.Str(),
        "is_on_behalf": fields.Bool(),
        "on_behalf": fields.Str()
    })
    @marshal_with(EventRegistrationSchema)
    def post(self, **kwargs):
        try:
            param = dict()
            param['api'] = "/api/v1/event-registration"
            param['method'] = "POST"
            args = request.args
            result = EventRegistrationHelpers(**param).create(kwargs)
            return result
        except Exception as e:
            print(e)
            return Response(
                json.dumps(str(e)),
                status=http.client.INTERNAL_SERVER_ERROR,
                mimetype='application/json'
            )
        
    @use_kwargs({
        "event_id": fields.Int(),
        "reg_id": fields.Int(),
    })
    def put(self, **kwargs):
        try:
            param = dict()
            args = request.args
            param['api'] = "/api/v1/event-registration"
            param['method'] = "PUT"
            print(kwargs)
            result = EventRegistrationHelpers(**param).create_qr(args)
            return result
        except Exception as e:
            return Response(
                json.dumps(str(e)),
                status=http.client.INTERNAL_SERVER_ERROR,
                mimetype='application/json'
            )
        
    def get(self, **kwargs):
        try:
            param = dict()
            args = request.args
            param['api'] = "/api/v1/event-registration"
            param['method'] = "GET"
            status, result = EventRegistrationHelpers(**param).registration_detail(args.to_dict())
            return result
        except Exception as e:
            print(e)
            return Response(
                json.dumps(str(e)),
                status=http.client.INTERNAL_SERVER_ERROR,
                mimetype='application/json'
            )
        
    ## PUT or PATCH for scan