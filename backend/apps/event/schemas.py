from marshmallow import Schema, ValidationError, fields, validates
from marshmallow_enum import EnumField
from apps import ma
from apps.event.models import (
    EventModel,
    EventLineModel,
    EventRegistrationModel,
    EventSouvenirClaimModel,
    # Enum
    RegistrationType
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
    registration_type = EnumField(RegistrationType, by_value=True)
    class Meta:
        model = EventRegistrationModel

        fields = ('id', 'registration_id', 'registration_type', 'name', 'email', 'phone', 'on_behalf', 'institution')

class ListEventRegistrationSchema(ma.SQLAlchemyAutoSchema):
    data = fields.Nested(EventRegistrationSchema, many=True)
    limit = fields.Int(allow_none=True)
    offset = fields.Int(allow_none=True)
    keywords = fields.Str(allow_none=True)
    total = fields.Int()

    class Meta:
        model = EventRegistrationModel

class EventSouvenirClaimSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventSouvenirClaimModel