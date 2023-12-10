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

class ListEventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventModel
    

class EventLineSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventLineModel


class EventRegistrationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventRegistrationModel

class ListEventRegistrationSchema(ma.SQLAlchemyAutoSchema):
    data = fields.Nested(EventRegistrationSchema, many=True)
    limit = fields.Int(allow_none=True)
    offset = fields.Int(allow_none=True)
    keywords = fields.Str(allow_none=True)
    total = fields.Int()

    class Meta:
        model = EventRegistrationModel

class EventSouvenirClaimModel(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventSouvenirClaimModel