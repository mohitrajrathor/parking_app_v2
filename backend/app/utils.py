# utility logic

# imports
from .extensions import db


def create_models():
    from .models import Admin, User, Parking, Slot, Review, Payment

    db.create_all()


def populate():
    from .populate import (
        add_Admin,
        add_test_user,
        add_test_parking_and_slots,
        add_test_payment,
        add_test_reservation,
        add_test_review,
    )

    add_Admin()
    add_test_user()
    add_test_parking_and_slots()
    add_test_reservation()
    add_test_review()
    add_test_payment()
