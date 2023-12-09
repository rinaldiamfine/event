from marshmallow import Schema, ValidationError, fields, validates
from marshmallow_enum import EnumField
from apps import ma
from apps.event.models import (
    EventModel,
    EventLineModel,
    EventRegistrationModel,
    EventSouvenirClaimModel
)

class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventModel

class EventListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventModel
    

class EventLineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventLineModel

class EventRegistrationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventRegistrationModel

class EventSouvenirClaimModel(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventSouvenirClaimModel