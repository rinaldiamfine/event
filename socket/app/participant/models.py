# from sqlalchemy import  Column, Integer, String
# from config import Base
from enum import Enum
from pydantic import BaseModel, Field

class RegistrationType(Enum):
    AUDIENCE = u'Audience'
    SPEAKER = u'Speaker'

class ParticipantModel(BaseModel):
    id: int
    name: str
    institution: str
    