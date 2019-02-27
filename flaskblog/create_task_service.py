from flaskblog import db
from flaskblog.models import Task


class CreateTaskService:

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def perform(self):

        new_task = Task(
            title=self.title,
            content=self.content
        )

        db.session.add(new_task)
        db.session.commit()
