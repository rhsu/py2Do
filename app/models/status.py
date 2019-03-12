from app import db
from datetime import datetime


class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow
    )
    is_deleted = db.Column(db.Boolean, nullable=False, default=False)
