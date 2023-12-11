from apps.tools.base_model import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy as sa
from apps import db
from enum import Enum

class RegistrationType(Enum):
    AUDIENCE = u'Audience'
    SPEAKER = u'Speaker'

class EventModel(BaseModel):
    __tablename__ = 'events'

    code = sa.Column(sa.String(50), nullable=False)
    name = sa.Column(sa.String(50), nullable=False)
    sequence = sa.Column(sa.Integer(), nullable=False, default=1)
    event_date = sa.Column(sa.DateTime())
    event_time = sa.Column(sa.String(50))
    venue = sa.Column(sa.String(50))
    created_uid = sa.Column(sa.Integer(), nullable=False)
    updated_uid = sa.Column(sa.Integer(), nullable=False)
    is_deleted = sa.Column(sa.Boolean)
    invitation_ids = relationship("EventInvitationModel", back_populates="event")
    registration_ids = relationship("EventRegistrationModel", back_populates="event")
    event_line_ids = relationship("EventLineModel", back_populates="event")

    def __repr__(self):
        return '<id : %s>' % (self.id)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self

        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def add_flush(self):
        try:
            db.session.add(self)
            db.session.flush()
            return self

        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        
class EventLineModel(BaseModel):
    __tablename__ = 'event_lines'

    event_id = sa.Column(sa.Integer(), sa.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    event = relationship("EventModel", back_populates="event_line_ids")
    name = sa.Column(sa.String(50), nullable=False)
    souvenir_cupons = sa.Column(sa.Integer(), nullable=True)
    created_uid = sa.Column(sa.Integer(), nullable=False)
    updated_uid = sa.Column(sa.Integer(), nullable=False)
    souvenir_claim_ids = relationship("EventSouvenirClaimModel", back_populates="event_line")

    def __repr__(self):
        return '<id : %s>' % (self.id)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self

        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def add_flush(self):
        try:
            db.session.add(self)
            db.session.flush()
            return self

        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        
class EventInvitationModel(BaseModel):
    __tablename__ = 'event_invitations'

    event_id = sa.Column(sa.Integer(), sa.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    event = relationship("EventModel", back_populates="invitation_ids")
    name = sa.Column(sa.String(50), nullable=False)
    email = sa.Column(sa.String(150), nullable=False)
    phone = sa.Column(sa.String(20), nullable=True)
    on_behalf = sa.Column(sa.String(50), nullable=True)
    created_uid = sa.Column(sa.Integer(), nullable=False)
    updated_uid = sa.Column(sa.Integer(), nullable=False)

    def __repr__(self):
        return '<id : %s>' % (self.id)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self

        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def add_flush(self):
        try:
            db.session.add(self)
            db.session.flush()
            return self

        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        
class EventRegistrationModel(BaseModel):
    __tablename__ = 'event_registrations'

    event_id = sa.Column(sa.Integer(), sa.ForeignKey('events.id', ondelete='CASCADE'), nullable=False)
    event = relationship("EventModel", back_populates="registration_ids")
    registration_id = sa.Column(sa.String(50), nullable=True)
    registration_type = sa.Column(sa.Enum(RegistrationType, name='registration_type'))
    uuid = sa.Column(sa.String(50), nullable=True)
    name = sa.Column(sa.String(50), nullable=False)
    email = sa.Column(sa.String(150), nullable=False)
    phone = sa.Column(sa.String(20), nullable=True)
    on_behalf = sa.Column(sa.String(50), nullable=True)
    created_uid = sa.Column(sa.Integer(), nullable=False)
    updated_uid = sa.Column(sa.Integer(), nullable=False)
    souvenir_claim_ids = relationship("EventSouvenirClaimModel", back_populates="event_registration")

    def __repr__(self):
        return '<id : %s>' % (self.id)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self

        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def add_flush(self):
        try:
            db.session.add(self)
            db.session.flush()
            return self

        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        
class EventSouvenirClaimModel(BaseModel):
    __tablename__ = 'event_souvenir_claims'

    event_registration_id = sa.Column(sa.Integer(), sa.ForeignKey('event_registrations.id', ondelete='CASCADE'), nullable=False)
    event_registration = relationship("EventRegistrationModel", back_populates="souvenir_claim_ids")
    event_line_id = sa.Column(sa.Integer(), sa.ForeignKey('event_lines.id', ondelete='CASCADE'), nullable=False)
    event_line = relationship("EventLineModel", back_populates="souvenir_claim_ids")
    date_claim = sa.Column(sa.DateTime(), nullable=False)
    created_uid = sa.Column(sa.Integer(), nullable=False)
    updated_uid = sa.Column(sa.Integer(), nullable=False)

    def __repr__(self):
        return '<id : %s>' % (self.id)

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return self

        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def add_flush(self):
        try:
            db.session.add(self)
            db.session.flush()
            return self

        except Exception as e:
            db.session.rollback()
            raise Exception(e)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return True

        except Exception as e:
            db.session.rollback()
            raise Exception(e)
        