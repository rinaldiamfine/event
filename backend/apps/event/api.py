from flask_restful import Api, Resource, reqparse
from apps import app
from flask_apispec import MethodResource, marshal_with, use_kwargs
from apps.event.helpers import (
    EventHelpers,
    EventLineHelpers,
    EventRegistrationHelpers,
    EventSouvenirClaimHelpers,
    CouponHelpers
)
from apps.event.schemas import (
    EventSchema,
    EventLineSchema,
    EventRegistrationSchema,
    ListEventRegistrationSchema,
    EventSouvenirClaimSchema
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
        "venue": fields.Str(),
        "event_date": fields.DateTime(),
        "event_time": fields.Str(),
    })
    @marshal_with(EventSchema)
    def post(self, **kwargs):
        try:
            param = dict()
            param['api'] = "/api/v1/events"
            param['method'] = "POST"
            status, result = EventHelpers(**param).create(kwargs)
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
        
    def get(self, **kwargs):
        try:
            params = request.args.to_dict()
            status, result = EventHelpers().list(params)
            if (status == False):
                return Response(
                    json.dumps({
                        "success": False,
                        "message": "Failed to fetch the event",
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
    

class EventLineApi(MethodResource):
    @use_kwargs({
        "name": fields.Str(),
        "event_id": fields.Int(),
        "souvenir_cupons": fields.Int(),
    })
    @marshal_with(EventLineSchema)
    def post(self, **kwargs):
        try:
            param = dict()
            param['api'] = "/api/v1/event-lines"
            param['method'] = "POST"
            status, result = EventLineHelpers(**param).create(kwargs)
            if (status == False):
                return Response(
                    json.dumps({
                        "success": False,
                        "message": "Failed to create the event lines",
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


class EventRegistrationApi(MethodResource):
    @use_kwargs({
        "event_id": fields.Int(),
        "name": fields.Str(),
        "phone": fields.Str(),
        "email": fields.Str(),
        "institution": fields.Str(),
        "on_behalf": fields.Str(required=False),
        "type": fields.Str()
    })
    def post(self, **kwargs):
        try:
            param = dict()
            param['api'] = "/api/v1/event-registrations"
            param['method'] = "POST"
            status, result = EventRegistrationHelpers(**param).create(kwargs)
            if (status == False):
                return Response(
                    json.dumps({
                        "success": False,
                        "message": "Failed to register the participant",
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
            print(e)
            return Response(
                json.dumps(str(e)),
                status=http.client.INTERNAL_SERVER_ERROR,
                mimetype='application/json'
            )
        
    @use_kwargs({
        "is_attendance": fields.Bool(),
        "offset": fields.Str(),
        "limit": fields.Str(),
        "keywords": fields.Str(),
    }, locations=['query'])
    # @marshal_with(ListEventRegistrationSchema)
    def get(self, **kwargs):
        try:
            param = dict()
            args = request.args
            param['api'] = "/api/v1/event-registrations"
            param['method'] = "GET"
            status, result = EventRegistrationHelpers(**param).list(args.to_dict())
            if (status == False):
                return Response(
                    json.dumps({
                        "success": False,
                        "message": "Failed to get the participant",
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
            print(e)
            return Response(
                json.dumps(str(e)),
                status=http.client.INTERNAL_SERVER_ERROR,
                mimetype='application/json'
            )
        
    ## PUT or PATCH for scan

class EventRegistrationDetailApi(MethodResource):
    def get(self, uid):
        param = dict()
        param['api'] = "/api/v1/event-registrations/{}".format(str(uid))
        param['method'] = "GET"
        status, result = EventRegistrationHelpers(**param).detail(uid)
        print(result, status)
        return result

class EventSouvenirClaimApi(MethodResource):
    @use_kwargs({
        "registration_id": fields.Str(),
        "event_line_id": fields.Int(),
    })
    @marshal_with(EventSouvenirClaimSchema)
    def post(self, **kwargs):
        param = dict()
        param['api'] = "/api/v1/events"
        param['method'] = "POST"
        status, result = EventSouvenirClaimHelpers(**param).create(kwargs)
        return result
    

class EventRegistrationCheckinApi(MethodResource):
    @use_kwargs({
        "coupon": fields.Str(),
        "committee_id": fields.Int(),
    })
    def post(self, **kwargs):
        try:
            param = dict()
            param['api'] = "/api/v1/participant/checkin"
            param['method'] = "POST"
            status, result = CouponHelpers(**param).checkin(kwargs)
            if (status == False):
                return Response(
                    json.dumps({
                        "success": False,
                        "message": "Failed to checkin",
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
            print(e)
            return Response(
                json.dumps(str(e)),
                status=http.client.INTERNAL_SERVER_ERROR,
                mimetype='application/json'
            )
        
class EventCouponApi(MethodResource):
    @use_kwargs({
        "coupon": fields.Str(),
        "committee_id": fields.Int(),
    })
    def post(self, **kwargs):
        try:
            param = dict()
            param['api'] = "/api/v1/coupon"
            param['method'] = "POST"
            status, result = CouponHelpers(**param).claim_coupons(kwargs)
            if (status == False):
                return Response(
                    json.dumps({
                        "success": False,
                        "message": "Failed claim the coupon",
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
            print(e)
            return Response(
                json.dumps(str(e)),
                status=http.client.INTERNAL_SERVER_ERROR,
                mimetype='application/json'
            )