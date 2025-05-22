# to populate data

# imports
from ..extensions import db


def add_Admin():
    """
    add admin data
    """
    from .admin import Admin

    if not Admin.query.filter_by(username="admin").first():
        admin = Admin(username="admin")
        admin.set_password("Admin@1234")
        db.session.add(admin)
        db.session.commit()


def add_test_user():
    """
    add user dummy data for testing
    """
    from .user import User

    if not User.query.filter_by(email="test@parkly.com").first():
        user = User(email="test@parkly.com")
        user.set_password("Test@123")
        db.session.add(user)
        db.session.commit()
