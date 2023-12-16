from flask_restful import Api
from flask import Blueprint
from apps import app
from apps.event.api import (
    EventApi,
    EventLineApi,
    EventRegistrationApi,
    EventRegistrationDetailApi,
    EventRegistrationDetailSocket,
    EventSouvenirClaimApi,

    EventRegistrationCheckinApi,
    EventCouponApi,
)
from flask_swagger import swagger

event_blueprint = Blueprint(
    'Events', __name__, url_prefix='/api/v1/event'
)
event_line_blueprint = Blueprint(
    'Event Lines', __name__, url_prefix='/api/v1/event-line'
)
event_registration_blueprint = Blueprint(
    'Event Registration', __name__, url_prefix='/api/v1/participant'
)
event_souvenir_claim_blueprint = Blueprint(
    'Event Souvenir', __name__, url_prefix='/api/v1/souvenir'
)
coupon_blueprint = Blueprint(
    'Coupon', __name__, url_prefix='/api/v1/coupon'
)

event_api = Api(event_blueprint)
event_api.add_resource(EventApi, '')

event_line_api = Api(event_line_blueprint)
event_line_api.add_resource(EventLineApi, '')

event_registration_api = Api(event_registration_blueprint)
event_registration_api.add_resource(EventRegistrationApi, '')
event_registration_api.add_resource(EventRegistrationCheckinApi, '/checkin')

event_registration_api.add_resource(EventRegistrationDetailApi, '/<int:uid>')
event_registration_api.add_resource(EventRegistrationDetailSocket, '/<int:event>/<int:uid>')

event_souvenir_claim_api = Api(event_souvenir_claim_blueprint)
event_souvenir_claim_api.add_resource(EventSouvenirClaimApi, '')


coupon_api = Api(coupon_blueprint)
coupon_api.add_resource(EventCouponApi, '')

