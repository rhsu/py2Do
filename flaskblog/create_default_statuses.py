from flaskblog import db
from flaskblog.models import Status


class CreateDefaultStatuses:

    def create_default(self):
        status_strings = ['Not Started', 'In Progress', 'Done']
        for status_string in status_strings:
            new_status = Status(
                title=status_string
            )
            db.session.add(new_status)
            db.session.commit()
