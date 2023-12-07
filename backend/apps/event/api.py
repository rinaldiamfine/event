from flask_restful import Api, Resource, reqparse
from flask import Blueprint
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
    })
    @marshal_with(EventSchema)
    def post(self, **kwargs):
        try:
            param = dict()
            param['api'] = "/api/v1/events"
            param['method'] = "POST"
            result = EventHelpers(**param).create(kwargs)
            return result
        except Exception as e:
            return Response(
                json.dumps(str(e)),
                status=http.client.INTERNAL_SERVER_ERROR,
                mimetype='application/json'
            )

    # @use_kwargs({
    #     "user_id": fields.Int(),
    #     "offset": fields.Str(),
    #     "limit": fields.Str(),
    #     "keywords": fields.Str(),
    # }, locations=['query'])
    # @marshal_with(TicketListSchema)
    # def get(self, **kwargs):
    #     try:
    #         param = dict()
    #         param['api'] = "/api/v1/tickets"
    #         param['method'] = "GET"
    #         result = TicketHelpers(**param).list(kwargs)
    #         return result

    #     except Exception as e:
    #         return Response(
    #             json.dumps(str(e)),
    #             status=http.client.INTERNAL_SERVER_ERROR,
    #             mimetype='application/json'
    #         )
        
    # @use_kwargs({
    #     "id": fields.Int(),
    #     "user_id": fields.Int(),
    #     "name": fields.Str(),
    #     "description": fields.Str(),
    #     "status_id": fields.Int(),
    #     "category_id": fields.Int(),
    # })
    # @marshal_with(TicketSchema)
    # def put(self, **kwargs):
    #     param = dict()
    #     param['api'] = "/api/v1/tickets"
    #     param['method'] = "PUT"
    #     result = TicketHelpers(**param).update(kwargs)
    #     return result


class EventRegistrationApi(MethodResource):
    @use_kwargs({
        "event_id": fields.Int(),
        "reg_no": fields.Str(),
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
            result = EventRegistrationHelpers(**param).create(kwargs)
            return result
        except Exception as e:
            print(e)
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
            # result = EventRegistrationHelpers(**param).create(kwargs)
            return True
        except Exception as e:
            print(e)
            return Response(
                json.dumps(str(e)),
                status=http.client.INTERNAL_SERVER_ERROR,
                mimetype='application/json'
            )

        
    