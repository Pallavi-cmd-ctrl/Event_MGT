# EventEase

A complete Flask and SQLite event-management demo. It includes customer registration, a multi-step event booking flow, vendor registration with image upload, a vendor dashboard, and a safe demo payment screen.

## Run it

1. Create and activate a virtual environment.
2. Install packages: `pip install -r requirements.txt`
3. Optionally copy `.env.example` to `.env` and replace the secret key.
4. Add the supplied demo services and vendor: `python seed.py`
5. Start the app: `python app.py`
6. Open `http://127.0.0.1:5000`.

Demo vendor login: `vendor@eventease.test` / `vendor123`.

## Project map

- `app.py` creates the Flask application.
- `models.py` contains User, Service, VendorProfile, and Booking models.
- `routes.py` contains all customer and vendor routes.
- `seed.py` creates image-backed services and a demo vendor.
- `static/images/services/` has local SVG image placeholders. Replace any SVG with a same-named `.jpg`/`.png` and update its path in `seed.py` if desired.

Payments are intentionally simulated; do not collect or store real card details in this demo.
