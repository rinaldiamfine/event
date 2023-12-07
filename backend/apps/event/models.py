from apps.tools.base_model import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy as sa
from apps import db

class Event(BaseModel):
    __tablename__ = 'event'

    code = sa.Column(sa.String(50), nullable=False)
    name = sa.Column(sa.String(50), nullable=False)
    registration_ids = relationship("EventRegistration", back_populates="event")


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
        

class EventRegistration(BaseModel):
    __tablename__ = 'event_registration'

    event_id = sa.Column(sa.Integer(), sa.ForeignKey('event.id', ondelete='CASCADE'), nullable=False)
    event = relationship("Event", back_populates="registration_ids")

    reg_no = sa.Column(sa.String(50), nullable=False)
    name = sa.Column(sa.String(50), nullable=False)
    email = sa.Column(sa.String(150), nullable=False)
    phone = sa.Column(sa.String(20), nullable=False)
    is_on_behalf = sa.Column(sa.Boolean, default=False)
    on_behalf = sa.Column(sa.String(50), nullable=False)

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