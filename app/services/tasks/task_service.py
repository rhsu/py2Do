from app import db
from app.models import Task


class TaskService:

    def get(self):
        return Task.query.filter_by(is_deleted=False).all()

    def post(self, title, content, status_id):
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
        task = Task.query.filter_by(id=id).first()

        task.title = title
        task.content = content
        task.status_id = status_id

        db.session.add(task)
        db.session.commit()
        return task
