from flask_restful import Api
from flask import Blueprint

from apps.event.api import (
    EventApi,
    EventRegistrationApi
)
from flask_swagger import swagger

event_blueprint = Blueprint(
    'event', __name__, url_prefix='/api/v1/events'
)
event_registration_blueprint = Blueprint(
    'event-registration', __name__, url_prefix='/api/v1/event-registration'
)

event_api = Api(event_blueprint)
event_api.add_resource(EventApi, '')

event_registration_api = Api(event_registration_blueprint)
event_registration_api.add_resource(EventRegistrationApi, '')
