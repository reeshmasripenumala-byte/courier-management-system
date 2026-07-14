from database import db
from datetime import date, timedelta


# ---------------- User Model ----------------
class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    mobile = db.Column(db.String(15), nullable=False)

    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<User {self.name}>"


# ---------------- Shipment Model ----------------
class Shipment(db.Model):
    __tablename__ = "shipments"

    id = db.Column(db.Integer, primary_key=True)

    sender_name = db.Column(db.String(100), nullable=False)

    receiver_name = db.Column(db.String(100), nullable=False)

    source = db.Column(db.String(100), nullable=False)

    destination = db.Column(db.String(100), nullable=False)

    weight = db.Column(db.Float, nullable=False)

    tracking_id = db.Column(db.String(20), unique=True, nullable=False)

    status = db.Column(
        db.String(50),
        default="Booked"
    )

    booking_date = db.Column(
        db.Date,
        default=date.today
    )

    delivery_date = db.Column(
        db.Date,
        default=lambda: date.today() + timedelta(days=5)
    )

    def __repr__(self):
        return f"<Shipment {self.tracking_id}>"