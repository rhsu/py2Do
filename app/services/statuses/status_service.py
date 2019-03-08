from app import db
from app.models import Status, Task


class StatusService:

    def get(self):
        return Status.query.all()

    def post(self, title):
        status = Status(title=title,)
        db.session.add(status)
        db.session.commit()
        return status

    def delete(self, id):
        """
        Check if there are any references to this status
        """
        count = Task.query.filter_by(status_id=id).count()
        if count == 0:
            Status.query.filter_by(id=id).delete()
            db.session.commit()
            return {"success": True}
        else:
            return {
                "success": False,
                "reason": "This status is being referenced"
            }

    def put(self, id, title):
        status = Status.query.filter_by(id=id).first()
        status.title = title
        db.session.add(status)
        db.session.commit()
        return status
