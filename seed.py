from app import app
from extensions import db
from models import Service, User, VendorProfile

SERVICES = [
    ("Accommodation", "accommodation", "Comfortable stays for every guest.", "images/services/accommodation.svg"),
    ("Bakery", "bakery", "Cakes and sweet moments made fresh.", "images/services/bakery.svg"),
    ("Birthday Parties", "birthday", "Joyful celebrations for every age.", "images/services/birthday.svg"),
    ("Catering", "catering", "Menus your guests will remember.", "images/services/catering.svg"),
    ("Decoration", "decoration", "Thoughtful décor with a personal touch.", "images/services/decoration.svg"),
    ("Event Planner", "event-planner", "Expert coordination from idea to applause.", "images/services/event-planner.svg"),
    ("Makeup", "makeup", "Professional artists for your big moment.", "images/services/makeup.svg"),
    ("Photographers", "photographers", "Memories captured beautifully.", "images/services/photographers.svg"),
    ("Photobooth", "photobooth", "Fun keepsakes for your guests.", "images/services/photobooth.svg"),
    ("Rental Accessories", "rental-accessories", "Furniture and finishing touches.", "images/services/rental-accessories.svg"),
    ("Tents", "tents", "Elegant outdoor event solutions.", "images/services/tents.svg"),
    ("Travel Management", "travel-management", "Smooth journeys for everyone.", "images/services/travel-management.svg"),
    ("Venue", "venue", "Spaces that set the scene.", "images/services/venue.svg"),
]

with app.app_context():
    db.create_all()
    if not Service.query.first():
        db.session.add_all(Service(name=n, slug=s, description=d, image=i) for n, s, d, i in SERVICES)
        db.session.commit()
    if not User.query.filter_by(email="vendor@eventease.test").first():
        user = User(name="Aarav Mehta", email="vendor@eventease.test", phone="9876543210", role="vendor")
        user.set_password("vendor123")
        vendor = VendorProfile(user=user, business_name="Golden Gatherings", description="A full-service team creating warm, memorable celebrations.", min_price=25000, max_price=120000, photo="images/vendor-placeholder.svg")
        vendor.services = Service.query.filter(Service.slug.in_(["catering", "decoration", "event-planner", "photographers"])).all()
        db.session.add(user); db.session.commit()
    print("Database seeded. Demo vendor: vendor@eventease.test / vendor123")
