# models functionalities

# imports
from ..extensions import db
from .admin import Admin
from .user import User


# expose them to use directly from models modules
__all__ = ["Admin", "User"]


def create_models():
    from .admin import Admin
    from .user import User

    db.create_all()


def populate():
    from .populate import add_Admin, add_test_user

    add_Admin()
    add_test_user()
