from flaskblog import db
from flaskblog.models import Task


class CreateTaskService:

    def __init__(self, title, content, status_id):
        self.title = title
        self.content = content
        self.status_id = status_id

    def perform(self):
        new_task = Task(
            title=self.title,
            content=self.content,
            status_id=self.status_id
        )
        db.session.add(new_task)
        db.session.commit()
        return new_task
