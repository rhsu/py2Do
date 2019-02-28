from flaskblog import db
from flaskblog.models import Task


class DeleteTaskService:

    def __init__(self, task_id):
        self.task_id = task_id

    def perform(self):
        Task.query.filter_by(id=self.task_id).delete()
        db.session.commit()
