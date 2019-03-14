from app import db
from app.models.status import Status
from app.models.task import Task


class StatusService:

    def get(self, id):
        return Status.query.filter_by(id=id, is_deleted=False).first()

    def get_list(self):
        return Status.query.filter_by(is_deleted=False).all()

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
            status = Status.query.filter_by(id=id).first()
            status.is_deleted = True
            db.session.commit()
            return {"success": True}
        else:
            return {
                "success": False,
                "errors": ["This status is being referenced"]
            }

    def put(self, id, title):
        status = Status.query.filter_by(id=id).first()
        status.title = title
        db.session.add(status)
        db.session.commit()
        return status
