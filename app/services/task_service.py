from app import db
from app.models.status import Status
from app.models.task import Task
from sqlalchemy.orm.exc import NoResultFound


class TaskService:

    def __init__(self):
        self.session = db.session()

    def get(self, id):
        return self.session.query(Task).filter_by(
            id=id, is_deleted=False).first()

    def get_list(self):
        return self.session.query(Task).filter_by(is_deleted=False).all()

    def post(self, title, content, status_id):
        if not self.valid_status(status_id):
            raise NoResultFound(
                "no result found for status_id %s" % (status_id))

        new_task = Task(
            title=title,
            content=content,
            status_id=status_id
        )

        self.session.add(new_task)
        self.session.commit()
        return new_task

    def delete(self, id):
        task = self.get(id)
        # TODO what happens if I try to delete something already deleted
        task.is_deleted = True
        self.session.commit()
        return {"success": True}

    def put(self, id, title, content, status_id):
        if not self.valid_status(status_id):
            raise NoResultFound(
                "no result found for status_id %s" % (status_id))

        task = self.get(id)
        # TODO what if task is None?

        task.title = title
        task.content = content
        task.status_id = status_id

        self.session.add(task)
        self.session.commit()
        return task

    def valid_status(self, status_id):
        return self.session.query(Status).filter_by(
            id=status_id,
            is_deleted=False
        ).count() == 1
