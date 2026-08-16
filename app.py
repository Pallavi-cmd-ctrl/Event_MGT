import os
from flask import Flask
from dotenv import load_dotenv
from extensions import db, login_manager

load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config.update(
        SECRET_KEY=os.getenv("SECRET_KEY", "development-key-change-me"),
        SQLALCHEMY_DATABASE_URI=os.getenv("DATABASE_URL", "sqlite:///eventease.db"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        UPLOAD_FOLDER=os.path.join(app.root_path, "static", "uploads"),
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,
    )
    os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)
    db.init_app(app)
    login_manager.init_app(app)
    from routes import main
    app.register_blueprint(main)
    with app.app_context():
        db.create_all()
    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
