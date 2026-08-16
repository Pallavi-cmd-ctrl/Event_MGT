from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(30))
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    vendor_profile = db.relationship("VendorProfile", back_populates="user", uselist=False, cascade="all, delete-orphan")
    bookings = db.relationship("Booking", back_populates="customer", foreign_keys="Booking.customer_id")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class Service(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False, unique=True)
    slug = db.Column(db.String(90), nullable=False, unique=True)
    description = db.Column(db.String(220), nullable=False)
    image = db.Column(db.String(180), nullable=False)
    vendors = db.relationship("VendorProfile", secondary="vendor_services", back_populates="services")


vendor_services = db.Table(
    "vendor_services",
    db.Column("vendor_id", db.Integer, db.ForeignKey("vendor_profile.id"), primary_key=True),
    db.Column("service_id", db.Integer, db.ForeignKey("service.id"), primary_key=True),
)


class VendorProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, unique=True)
    business_name = db.Column(db.String(140), nullable=False)
    description = db.Column(db.Text, nullable=False)
    min_price = db.Column(db.Float, nullable=False)
    max_price = db.Column(db.Float, nullable=False)
    photo = db.Column(db.String(240), default="images/vendor-placeholder.svg")
    is_approved = db.Column(db.Boolean, default=True, nullable=False)
    user = db.relationship("User", back_populates="vendor_profile")
    services = db.relationship("Service", secondary=vendor_services, back_populates="vendors")
    bookings = db.relationship("Booking", back_populates="vendor", foreign_keys="Booking.vendor_id")


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    vendor_id = db.Column(db.Integer, db.ForeignKey("vendor_profile.id"), nullable=False)
    event_type = db.Column(db.String(100), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    guests = db.Column(db.Integer, nullable=False)
    venue = db.Column(db.String(160), nullable=False)
    notes = db.Column(db.Text)
    selected_services = db.Column(db.String(500), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(30), nullable=False, default="Pending")
    payment_status = db.Column(db.String(30), nullable=False, default="Unpaid")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    customer = db.relationship("User", back_populates="bookings", foreign_keys=[customer_id])
    vendor = db.relationship("VendorProfile", back_populates="bookings", foreign_keys=[vendor_id])
