from flask_restful import Api
from flask import Blueprint
from apps import app
from apps.event.api import (
    EventApi,
    EventLineApi,
    EventRegistrationApi
)
from flask_swagger import swagger

event_blueprint = Blueprint(
    'Events', __name__, url_prefix='/api/v1/events'
)
event_line_blueprint = Blueprint(
    'Event Lines', __name__, url_prefix='/api/v1/event-lines'
)
event_registration_blueprint = Blueprint(
    'Event Registration', __name__, url_prefix='/api/v1/event-registrations'
)

event_api = Api(event_blueprint)
event_api.add_resource(EventApi, '')
event_line_api = Api(event_line_blueprint)
event_line_api.add_resource(EventLineApi, '')
event_registration_api = Api(event_registration_blueprint)
event_registration_api.add_resource(EventRegistrationApi, '')
