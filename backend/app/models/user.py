# to handle user related data

# imports
from ..extensions import db
from uuid import uuid4
from werkzeug.security import check_password_hash, generate_password_hash


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unique_id = db.Column(db.String, nullable=False, default=str(uuid4()))
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __repr__(self) -> None:
        return f"User <email : {self.email}>"

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> None:
        return check_password_hash(self.password, password)
