from flask_restful import Api
from flask import Blueprint
from apps import app
from apps.committee.api import (
    LoginApi
)
from flask_swagger import swagger

committee_blueprint = Blueprint(
    'Committee', __name__, url_prefix='/api/v1//comitte'
)

authentication_api = Api(committee_blueprint)
authentication_api.add_resource(LoginApi, '/login')
