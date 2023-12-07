from marshmallow import Schema, ValidationError, fields, validates
from marshmallow_enum import EnumField
from apps import ma
from apps.event.models import (
    Event,
    EventRegistration
)

class EventSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Event

class EventRegistrationSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = EventRegistration