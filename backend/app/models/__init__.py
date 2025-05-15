# models functionalities

from ..extensions import db


def create_models():
    from .admin import Admin

    db.create_all()


def add_Admin():
    from .admin import Admin

    if not Admin.query.filter_by(username="admin").first():
        admin = Admin(username="admin")
        admin.set_password("Admin@1234")
        db.session.add(admin)
        db.session.commit()


def populate():
    add_Admin()
