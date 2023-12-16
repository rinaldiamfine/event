from apps.tools.base_model import BaseModel
from sqlalchemy.orm import relationship
import sqlalchemy as sa
from apps import db
from enum import Enum

class CommitteeModel(BaseModel):
    __tablename__ = 'committee'

    name = sa.Column(sa.String(50), nullable=False)
    username = sa.Column(sa.String(50), nullable=False)
    password = sa.Column(sa.String(50), nullable=False)
    role = sa.Column(sa.String(50), nullable=False)
    created_uid = sa.Column(sa.Integer(), nullable=False)
    updated_uid = sa.Column(sa.Integer(), nullable=False)
    is_deleted = sa.Column(sa.Boolean)

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