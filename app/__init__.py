from __future__ import annotations

from flask import Flask
from dotenv import load_dotenv

from config import Config

from .models import db
from .routes import main_bp
from .seed import seed_reference_data


def create_app() -> Flask:
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(main_bp)

    with app.app_context():
        db.create_all()
        seed_reference_data()

    return app
