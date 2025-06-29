#  models


# imports
from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime as dt
from zoneinfo import ZoneInfo
from uuid import uuid4


class Admin(db.Model):
    __tablename__ = "admins"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=True)
    password = db.Column(db.String, nullable=False)

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"Admin <username: {self.username}>"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    unique_id = db.Column(db.String, nullable=False, default=str(uuid4()))
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    dob = db.Column(db.Date, nullable=False)
    profession = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    email_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    join_time = db.Column(
        db.DateTime, nullable=False, default=dt.now(ZoneInfo("Asia/Kolkata"))
    )

    def __repr__(self) -> str:
        return f"User <email : {self.email}>"

    def set_password(self, password: str) -> None:
        self.password = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password, password)

    def to_dict(self):

        reservations = [res.to_dict() for res in self.reservations]
        reviews = [rw.to_dict() for rw in self.reviews]


        return {
            "id": self.id,
            "unique_id": self.unique_id,
            "email": self.email,
            "name": self.name,
            "dob": self.dob.strftime("%Y-%m-%d") if self.dob else None,
            "profession": self.profession,
            "address": self.address,
            "pincode": self.pincode,
            "phone": self.phone,
            "email_confirmed": self.email_confirmed,
            "join_time": self.join_time.strftime("%d-%m-%yT%H:%M%S") if self.join_time else None,
            "bookings": reservations,
            "total_bookings": len(reservations),
            "active_bookings": len([res for res in reservations if res.get("is_booked")]),
            "reviews": reviews,
            "total_reviews": len(reviews)
        }


class Parking(db.Model):
    __tablename__ = "parkings"

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, unique=True, nullable=False
    )
    name = db.Column(db.String, nullable=False)
    address = db.Column(db.String, nullable=False)
    pincode = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False)
    lat = db.Column(db.Float, nullable=False)
    long = db.Column(db.Float, nullable=False)
    fee = db.Column(db.Float, nullable=False)
    create_time: dt = db.Column(
        db.DateTime, nullable=False, default=dt.now(tz=ZoneInfo("Asia/Kolkata"))
    )
    slots_num = db.Column(db.Integer, nullable=False)

    slots = db.relationship(
        "Slot",
        backref="parking",
        lazy=True,
        cascade="all, delete-orphan",
        foreign_keys="Slot.parking_id",
    )
    reservations = db.relationship("Reservation", backref="parking", lazy=True)
    reviews = db.relationship("Review", backref="parking", lazy=True)

    def __repr__(self):
        return f"<Parking lat-{self.lat} | long-{self.long}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "pincode": self.pincode,
            "phone": self.phone,
            "lat": self.lat,
            "long": self.long,
            "fee": self.fee,
            "create_time": self.create_time.strftime("%d-%m-%yT%H:%M%S"),
            "slots_num": self.slots_num,
            "slots": [slot.to_dict() for slot in self.slots],
            "booked": Slot.query.filter_by(
                parking_id=self.id, is_occupied=True
            ).count(),
            "reviews_count": Review.query.filter_by(parking_id=self.id).count(),
            "reviews": [rv.to_dict() for rv in self.reviews],
        }


class Slot(db.Model):
    __tablename__ = "slots"

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    parking_id = db.Column(db.Integer, db.ForeignKey("parkings.id"), nullable=False)
    serial_id = db.Column(
        db.String, nullable=False, unique=True
    )  # eg PR0SL0 -> PR0 refer to parking id 0 and SL0 refer to slot number 0
    is_occupied = db.Column(db.Boolean, nullable=False, default=False)

    def __repr__(self):
        return f"<Slot {self.serial_id} - Occupied: {self.is_occupied}>"

    def to_dict(self):
        return {
            "id": self.id,
            "parking_id": self.parking_id,
            "serial_id": self.serial_id,
            "is_occupied": self.is_occupied,
        }


class Reservation(db.Model):
    __tablename__ = "reservations"

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    parking_id = db.Column(
        db.Integer, db.ForeignKey("parkings.id", ondelete="SET NULL"), nullable=True
    )
    slot_id = db.Column(
        db.Integer, db.ForeignKey("slots.id", ondelete="SET NULL"), nullable=True
    )
    start_time = db.Column(
        db.DateTime, nullable=False, default=dt.now(ZoneInfo("Asia/Kolkata"))
    )
    is_booked = db.Column(
        db.Boolean, nullable=False, default=True
    )
    leave_time = db.Column(db.DateTime, nullable=False)


    user = db.relationship("User", backref="reservations", lazy=True)
    slot = db.relationship("Slot", backref="reservations", lazy=True)

    def __repr__(self):
        return f"<Reservation {self.id} - User {self.user_id}, Slot {self.slot_id}>"


    def to_dict(self):
        return {
            "id": self.id,
            "user": {
                "id": self.user.id,
                "name": self.user.name,
                "email": self.user.email,
            } if self.user else None,
            "parking": {
                "id": self.parking_id,
                "name": self.parking.name if getattr(self, "parking", None) else None,
                "fee": self.parking.fee if getattr(self, "parking", None) else None,
            } if self.parking_id else None,
            "slot": {
                "id": self.slot.id,
                "serial_id": self.slot.serial_id,
                "is_occupied": self.slot.is_occupied,
            } if self.slot else None,
            "start_time": self.start_time.strftime("%d-%m-%yT%H:%M%S") if self.start_time else None,
            "leave_time": self.leave_time.strftime("%d-%m-%yT%H:%M%S") if self.leave_time else None,
        }


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    parking_id = db.Column(
        db.Integer, db.ForeignKey("parkings.id", ondelete="SET NULL"), nullable=True
    )
    feedback = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    create_time = db.Column(
        db.DateTime, nullable=False, default=dt.now(ZoneInfo("Asia/Kolkata"))
    )

    user = db.relationship("User", backref="reviews", lazy=True)

    def __repr__(self):
        return f"<Review {self.id} - User {self.user_id}, Parking {self.parking_id}, Rating {self.rating}>"

    def to_dict(self):
        return {
            "id": self.id,
            "user": {
                "id": self.user.id,
                "name": self.user.name,
                "email": self.user.email,
            },
            "parking": {
                "id": self.parking.id if getattr(self, "parking", None) else self.parking_id,
                "name": self.parking.name if getattr(self, "parking", None) else None,
                "fee": self.parking.fee if getattr(self, "parking", None) else None,
            },
            "feedback": self.feedback,
            "rating": self.rating,
            "create_at": self.create_time.strftime("%d-%m-%yT%H:%M%S"),
        }


class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(
        db.Integer, primary_key=True, autoincrement=True, nullable=False, unique=True
    )
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    parking_id = db.Column(
        db.Integer, db.ForeignKey("parkings.id", ondelete="SET NULL"), nullable=True
    )
    reserve_id = db.Column(db.Integer, db.ForeignKey("reservations.id"), nullable=True)
    hour_used = db.Column(db.Integer, nullable=False)
    fee = db.Column(db.Float, nullable=False)
    cost = db.Column(db.Float, nullable=False)
    exit_time = db.Column(db.DateTime, nullable=False)

    user = db.relationship("User", backref="payments", lazy=True)
    parking = db.relationship("Parking", backref="payments", lazy=True)
    reservation = db.relationship(
        "Reservation", backref="payment", lazy=True, uselist=False
    )

    def __repr__(self):
        return f"<Payment {self.id} - User {self.user_id}, Cost {self.cost}>"
