from app import db
from datetime import datetime


class CustomFieldValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    custom_field_id = db.Column(
        db.Integer,
        db.ForeignKey('custom_field.id'),
        nullable=False
    )
    task_id = db.Column(
        db.Integer,
        db.ForeignKey('task.id'),
        nullable=False
    )
    value = db.Column(db.String(100))
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
