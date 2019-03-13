from app import db
from app.models.status import Status
from app.models.task import Task
from sqlalchemy.orm.exc import NoResultFound


class TaskService:

    def get(self):
        return Task.query.filter_by(is_deleted=False).all()

    def post(self, title, content, status_id):
        if not self.valid_status(status_id):
            raise NoResultFound(
                "no result found for status_id %s" % (status_id))

        new_task = Task(
            title=title,
            content=content,
            status_id=status_id
        )

        db.session.add(new_task)
        db.session.commit()
        return new_task

    def delete(self, id):
        task = Task.query.filter_by(id=id).first()
        task.is_deleted = True
        db.session.commit()
        return {"success": True}

    def put(self, id, title, content, status_id):
        if not self.valid_status(status_id):
            raise NoResultFound(
                "no result found for status_id %s" % (status_id))

        task = Task.query.filter_by(id=id).first()

        task.title = title
        task.content = content
        task.status_id = status_id

        db.session.add(task)
        db.session.commit()
        return task

    def valid_status(self, status_id):
        return Status.query.filter_by(id=status_id).count() == 1
