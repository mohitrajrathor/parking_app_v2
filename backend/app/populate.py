# to populate data

# imports
from .extensions import db
from datetime import datetime as dt, timedelta
from zoneinfo import ZoneInfo


def add_Admin():
    """
    add admin data
    """
    from .models import Admin

    if not Admin.query.filter_by(username="admin").first():
        admin = Admin(username="admin")
        admin.set_password("Admin@1234")
        db.session.add(admin)
        db.session.commit()


def add_test_parking_and_slots():
    """
    to add test parking
    """
    from .models import Parking
    from .models import Slot

    if not Parking.query.filter_by(name="Test Parking").first():
        parking = Parking(
            name="Test Parking",
            address="test area, city, state, country",
            pincode="654321",
            phone="9876543210",
            lat=24.58412446451834,
            long=76.17353439331056,
            hourly_fee=10,
            booking_fee=40,
            slots_num=10,
        )

        db.session.add(parking)
        db.session.commit()

        db.session.add_all(
            [
                Slot(parking_id=parking.id, serial_id=f"PR{parking.id}SL{i}")
                for i in range(1, parking.slots_num + 1)
            ]
        )
        db.session.commit()


def add_test_user():
    """
    to add user dummy data for testing
    """
    from .models import User

    if not User.query.filter_by(email="test@parkly.com").first():
        user = User(email="test@parkly.com")
        user.set_password("Test@123")
        user.name = "tester"
        user.dob = dt(year=2000, month=1, day=1)
        user.profession = "developer"
        user.address = "test address"
        user.pincode = "654321"
        user.phone = "9876543210"
        user.email_confirmed = True

        db.session.add(user)
        db.session.commit()


def add_test_reservation():
    from .models import Reservation

    if not Reservation.query.filter_by(user_id=1, parking_id=1, slot_id=1).first():
        rvsn = Reservation(
            user_id=1,
            parking_id=1,
            slot_id=1,
            is_booked=False,
            start_time=dt.now(ZoneInfo("Asia/Kolkata"))
            - timedelta(hours=5, minutes=45),
            leave_time=dt.now(ZoneInfo("Asia/Kolkata"))
            - timedelta(hours=3, minutes=12),
        )

        db.session.add(rvsn)
        db.session.commit()


def add_test_review():
    from .models import Review

    if not Review.query.filter_by(user_id=1, parking_id=1).first():

        rw = Review(
            user_id=1,
            parking_id=1,
            reservation_id=1,
            feedback="test parking is good!",
            rating=4,
        )

        db.session.add(rw)
        db.session.commit()


def add_test_payment():
    from .models import Payment

    if not Payment.query.filter_by(user_id=1, parking_id=1).first():

        pay = Payment(
            user_id=1,
            parking_id=1,
            reserve_id=1,
            fee=40,
            amount=40,
            payment_time=dt.now(ZoneInfo("Asia/Kolkata")),
            pay_for="booking",
        )

        db.session.add(pay)
        db.session.commit()

        pay = Payment(
            user_id=1,
            parking_id=1,
            reserve_id=1,
            fee=40,
            amount=40 * 3,
            payment_time=dt.now(ZoneInfo("Asia/Kolkata")) + timedelta(hours=3),
            pay_for="charge",
        )

        db.session.add(pay)
        db.session.commit()
