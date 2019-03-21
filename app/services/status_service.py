from app import db
from app.models.status import Status
from app.models.task import Task


class StatusService:

    def __init__(self):
        self.session = db.session()

    def get(self, id):
        return self.session.query(Status).filter_by(
            id=id, is_deleted=False).first()

    def get_list(self):
        return self.session.query(Status).filter_by(is_deleted=False).all()

    def post(self, title):
        status = Status(title=title)
        self.session.add(status)
        self.session.commit()
        return status

    def delete(self, id):
        """
        Check if there are any references to this status
        """
        count = self.session.query(Task).filter_by(status_id=id).count()
        if count == 0:
            status = self.session.query(Status).filter_by(id=id).first()
            # TODO what if status None?
            status.is_deleted = True
            self.session.commit()
            return {"success": True}
        else:
            return {
                "success": False,
                "errors": ["This status is being referenced"]
            }

    def put(self, id, title):
        status = self.get(id)
        # TODO what is status is None?
        status.title = title
        self.session.add(status)
        self.session.commit()
        return status
