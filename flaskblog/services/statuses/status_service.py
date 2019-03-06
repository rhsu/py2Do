from flaskblog import db
from flaskblog.models import Status


class StatusService:

    def get(self):
        return Status.query.all()

    def post(self, title):
        status = Status(title=title,)
        db.session.add(status)
        db.session.commit()
        return status

    def delete(self, id):
        Status.query.filter_by(id=id).delete()
        db.session.commit()

    def put(self, id, title):
        status = Status.query.filter_by(id=id).first()
        status.title = title
        db.session.add(status)
        db.session.commit()
        return status
