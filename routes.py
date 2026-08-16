import os
import uuid
from datetime import datetime
from functools import wraps
from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user
from werkzeug.utils import secure_filename
from extensions import db
from models import Booking, Service, User, VendorProfile

main = Blueprint("main", __name__)
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}


def vendor_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != "vendor":
            flash("That page is for vendor accounts.", "danger")
            return redirect(url_for("main.vendor_login"))
        return view(*args, **kwargs)
    return wrapped


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@main.route("/")
def home():
    services = Service.query.limit(6).all()
    return render_template("home.html", services=services)


@main.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    if request.method == "POST":
        name, email = request.form.get("name", "").strip(), request.form.get("email", "").strip().lower()
        phone, password = request.form.get("phone", "").strip(), request.form.get("password", "")
        if not name or not email or not phone or len(password) < 6:
            flash("Name, phone number, email, and a password of at least 6 characters are required.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "danger")
        else:
            user = User(name=name, email=email, phone=phone, role="user")
            user.set_password(password)
            db.session.add(user); db.session.commit()
            login_user(user)
            flash("Welcome to EventEase!", "success")
            return redirect(url_for("main.event_details"))
    return render_template("auth.html", mode="signup")


@main.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.vendor_dashboard" if current_user.role == "vendor" else "main.home"))
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email", "").strip().lower(), role="user").first()
        if user and user.check_password(request.form.get("password", "")):
            login_user(user, remember=bool(request.form.get("remember")))
            return redirect(request.args.get("next") or url_for("main.home"))
        flash("Incorrect email or password.", "danger")
    return render_template("auth.html", mode="login")


@main.route("/vendor/signup", methods=["GET", "POST"])
def vendor_signup():
    services = Service.query.order_by(Service.name).all()
    if current_user.is_authenticated:
        return redirect(url_for("main.vendor_dashboard" if current_user.role == "vendor" else "main.home"))
    if request.method == "POST":
        name, email = request.form.get("name", "").strip(), request.form.get("email", "").strip().lower()
        business, description = request.form.get("business_name", "").strip(), request.form.get("description", "").strip()
        chosen = [int(i) for i in request.form.getlist("services") if i.isdigit()]
        try:
            min_price, max_price = float(request.form.get("min_price", 0)), float(request.form.get("max_price", 0))
        except ValueError:
            min_price = max_price = 0
        if not all([name, email, business, description]) or len(request.form.get("password", "")) < 6 or not chosen or min_price <= 0 or max_price < min_price:
            flash("Complete every field, select a service, and enter a valid price range.", "danger")
        elif User.query.filter_by(email=email).first():
            flash("An account with that email already exists.", "danger")
        else:
            photo_path = "images/vendor-placeholder.svg"
            photo = request.files.get("photo")
            if photo and photo.filename:
                if not allowed_file(photo.filename):
                    flash("Use PNG, JPG, WEBP, or GIF for the business photo.", "danger")
                    return render_template("vendor_signup.html", services=services)
                filename = f"{uuid.uuid4().hex}_{secure_filename(photo.filename)}"
                photo.save(os.path.join(current_app.config["UPLOAD_FOLDER"], filename))
                photo_path = f"uploads/{filename}"
            user = User(name=name, email=email, phone=request.form.get("phone", "").strip(), role="vendor")
            user.set_password(request.form["password"])
            vendor = VendorProfile(user=user, business_name=business, description=description, min_price=min_price, max_price=max_price, photo=photo_path)
            vendor.services = Service.query.filter(Service.id.in_(chosen)).all()
            db.session.add(user); db.session.commit()
            login_user(user)
            flash("Your vendor profile is ready.", "success")
            return redirect(url_for("main.vendor_dashboard"))
    return render_template("vendor_signup.html", services=services)


@main.route("/vendor/login", methods=["GET", "POST"])
def vendor_login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form.get("email", "").strip().lower(), role="vendor").first()
        if user and user.check_password(request.form.get("password", "")):
            login_user(user, remember=bool(request.form.get("remember")))
            return redirect(url_for("main.vendor_dashboard"))
        flash("Incorrect vendor email or password.", "danger")
    return render_template("auth.html", mode="vendor_login")


@main.route("/logout")
@login_required
def logout():
    logout_user(); session.pop("event", None); session.pop("services", None)
    flash("You have been signed out.", "info")
    return redirect(url_for("main.home"))


@main.route("/services")
def services():
    return render_template("services.html", services=Service.query.order_by(Service.name).all())


@main.route("/plan-event", methods=["GET", "POST"])
@login_required
def event_details():
    if current_user.role == "vendor": return redirect(url_for("main.vendor_dashboard"))
    if request.method == "POST":
        date_string = request.form.get("event_date", "")
        try: datetime.strptime(date_string, "%Y-%m-%d")
        except ValueError:
            flash("Please choose a valid event date.", "danger")
            return render_template("event_details.html")
        session["event"] = {"event_type": request.form.get("event_type", "Celebration"), "event_date": date_string,
                            "guests": request.form.get("guests", "1"), "venue": request.form.get("venue", "").strip(), "notes": request.form.get("notes", "").strip()}
        return redirect(url_for("main.select_services"))
    return render_template("event_details.html", event=session.get("event", {}))


@main.route("/select-services", methods=["GET", "POST"])
@login_required
def select_services():
    if "event" not in session: return redirect(url_for("main.event_details"))
    services = Service.query.order_by(Service.name).all()
    if request.method == "POST":
        selected = [int(i) for i in request.form.getlist("services") if i.isdigit()]
        if not selected:
            flash("Select at least one service.", "danger")
        else:
            session["services"] = selected
            return redirect(url_for("main.available_vendors"))
    return render_template("select_services.html", services=services, selected=session.get("services", []))


@main.route("/vendors")
@login_required
def available_vendors():
    ids = session.get("services", [])
    if not ids: return redirect(url_for("main.select_services"))
    vendors = VendorProfile.query.join(VendorProfile.services).filter(Service.id.in_(ids), VendorProfile.is_approved.is_(True)).distinct().all()
    return render_template("vendors.html", vendors=vendors, selected_services=Service.query.filter(Service.id.in_(ids)).all())


@main.route("/booking/<int:vendor_id>/confirm", methods=["GET", "POST"])
@login_required
def booking_confirm(vendor_id):
    if "event" not in session or not session.get("services"): return redirect(url_for("main.event_details"))
    vendor = db.get_or_404(VendorProfile, vendor_id)
    selected = Service.query.filter(Service.id.in_(session["services"])).all()
    if request.method == "POST":
        event = session["event"]
        booking = Booking(customer=current_user, vendor=vendor, event_type=event["event_type"], event_date=datetime.strptime(event["event_date"], "%Y-%m-%d").date(), guests=int(event["guests"]), venue=event["venue"], notes=event["notes"], selected_services=", ".join(s.name for s in selected), total_amount=vendor.min_price)
        db.session.add(booking); db.session.commit()
        session["pending_booking"] = booking.id
        return redirect(url_for("main.payment", booking_id=booking.id))
    return render_template("booking_confirm.html", vendor=vendor, services=selected, event=session["event"])


@main.route("/payment/<int:booking_id>", methods=["GET", "POST"])
@login_required
def payment(booking_id):
    booking = db.get_or_404(Booking, booking_id)
    if booking.customer_id != current_user.id: abort(403)
    if request.method == "POST":
        method = request.form.get("payment_method", "")
        card_number = request.form.get("card_number", "").replace(" ", "")
        upi_id = request.form.get("upi_id", "").strip()
        if method == "card" and (not request.form.get("card_name") or len(card_number) < 12 or not request.form.get("expiry") or len(request.form.get("cvv", "")) < 3):
            flash("Complete the demo card details with a valid card number.", "danger")
        elif method == "upi" and ("@" not in upi_id or len(upi_id) < 5):
            flash("Enter a valid UPI ID, for example name@bank.", "danger")
        elif method not in {"card", "upi"}:
            flash("Choose Card or UPI to continue.", "danger")
        else:
            booking.payment_status, booking.status = "Paid", "Confirmed"
            db.session.commit()
            session.pop("event", None); session.pop("services", None); session.pop("pending_booking", None)
            return redirect(url_for("main.payment_success", booking_id=booking.id))
    return render_template("payment.html", booking=booking)


@main.route("/payment-success/<int:booking_id>")
@login_required
def payment_success(booking_id):
    booking = db.get_or_404(Booking, booking_id)
    if booking.customer_id != current_user.id: abort(403)
    return render_template("payment_success.html", booking=booking)


@main.route("/my-bookings")
@login_required
def my_bookings():
    if current_user.role == "vendor": return redirect(url_for("main.vendor_dashboard"))
    return render_template("my_bookings.html", bookings=Booking.query.filter_by(customer_id=current_user.id).order_by(Booking.event_date.desc()).all())


@main.route("/vendor/dashboard", methods=["GET", "POST"])
@vendor_required
def vendor_dashboard():
    vendor = current_user.vendor_profile
    if request.method == "POST":
        booking = db.get_or_404(Booking, int(request.form.get("booking_id", 0)))
        if booking.vendor_id != vendor.id: abort(403)
        action = request.form.get("action")
        if action in {"Accepted", "Declined"}:
            booking.status = action
            db.session.commit()
            flash(f"Booking {action.lower()}.", "success")
    bookings = Booking.query.filter_by(vendor_id=vendor.id).order_by(Booking.event_date).all()
    return render_template("vendor_dashboard.html", vendor=vendor, bookings=bookings)
