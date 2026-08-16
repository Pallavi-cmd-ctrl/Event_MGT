# EventEase – Event Management System

EventEase is a full-stack **event management web application** built using **Flask, SQLite, HTML, CSS, and JavaScript**.

The platform provides separate workflows for **customers and vendors**, allowing users to explore events, register for events, complete bookings, and manage vendor services through a dedicated dashboard.

## Features

### 👤 Customer Features

- User registration and login
- Secure session-based authentication
- Browse available events and services
- Multi-step event booking process
- Booking confirmation
- Demo payment workflow
- View booking details
- Responsive user interface

### 🏢 Vendor Features

- Vendor registration
- Vendor profile creation
- Vendor image upload
- Vendor dashboard
- Manage vendor/service information
- View event-related booking information

### 🎫 Event Management

- Event listing and management
- Event booking workflow
- Customer registration
- Vendor/service management
- Booking data stored in SQLite
- Seed data for demonstration

### 🔐 Security

- Password hashing
- Flask session management
- Environment variables for sensitive configuration
- Secret key stored outside source code
- `.gitignore` configured to prevent sensitive files from being committed

## Technology Stack

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web framework |
| Flask-SQLAlchemy | Database ORM |
| Flask-Login | Authentication |
| SQLite | Database |
| HTML5 | Page structure |
| CSS3 | Styling |
| JavaScript | Frontend interactions |
| Jinja2 | Server-side templates |
| Gunicorn | Production WSGI server |
| Git & GitHub | Version control |
| Render | Deployment |

## Project Structure

```text
EventEase-Final/
│
├── app.py
├── extensions.py
├── models.py
├── routes.py
├── seed.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
│
├── static/
│   ├── css/
│   ├── js/
│   └── images/
│
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    ├── register.html
    ├── dashboard.html
    └── ...
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Pallavi-cmd-ctrl/Event_MGT.git
cd Event_MGT
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
```

Activate it:

```powershell
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root.

Example:

```env
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///eventease.db
```

Do not commit `.env` to GitHub.

### 5. Initialize demo data

If seed data is required, run:

```bash
python seed.py
```

### 6. Run the application

```bash
python app.py
```

Open the application in your browser at:

```text
http://127.0.0.1:5000
```

## Deployment

The application can be deployed on **Render** as a Python Web Service.

### Build Command

```bash
pip install -r requirements.txt
```

### Start Command

```bash
gunicorn app:app
```

### Environment Variables

Configure the following variables in Render:

```text
SECRET_KEY=your-production-secret-key
DATABASE_URL=sqlite:///eventease.db
```

## Database

EventEase uses **SQLite** for database storage.

The application uses SQLAlchemy to manage database models and database operations.

For local development, the SQLite database can be created automatically by the application depending on the configured initialization logic.

> Note: SQLite on a cloud platform such as Render is suitable for a demonstration or college project, but production applications requiring persistent data should use a managed database such as PostgreSQL.

## Authentication

The application provides authentication for users and vendors.

Passwords are stored using secure password hashing rather than plain text.

Sessions are used to maintain authenticated users throughout the application.

## Demo Data

The project includes `seed.py`, which can be used to populate the application with sample events, vendors, or other demonstration data.

Run:

```bash
python seed.py
```

only when you want to initialize or reset the intended demo data.

## Environment Variables

The following environment variables are used:

| Variable | Description |
|---|---|
| `SECRET_KEY` | Flask application secret key |
| `DATABASE_URL` | Database connection URL |

Never commit real production secrets to the repository.

## Version Control

The project uses Git for version control.

Typical workflow:

```bash
git add .
git commit -m "Update project"
git push
```

The GitHub repository is:

**Pallavi-cmd-ctrl/Event_MGT**

## Future Improvements

- Online payment gateway integration
- PostgreSQL database for production
- Email notifications
- Event search and filtering
- Vendor rating and review system
- Admin dashboard
- Event ticket generation
- QR-code based event check-in
- Cloud-based image storage
- Improved analytics and reporting

## Project Purpose

EventEase was developed as an academic project to demonstrate the development and deployment of a web-based event management system using Python Flask and a relational database.

## License

This project is intended for educational and academic purposes.
