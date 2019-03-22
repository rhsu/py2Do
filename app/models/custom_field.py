from app import db
from datetime import datetime
from enum import Enum


class FieldTypes(Enum):
    TEXT = 1
    NUMBER = 2


class CustomField(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    field_type = db.Column(db.Integer, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
