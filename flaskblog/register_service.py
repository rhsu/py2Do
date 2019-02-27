from flaskblog import db
from flaskblog.models import User


class RegisterService:

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

    def perform(self):
        new_user = User(
            username=self.username,
            password=self.password,
            email=self.email
        )

        db.session.add(new_user)
        db.session.commit()
