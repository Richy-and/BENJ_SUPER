import os
import logging
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_babel import Babel
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.engine.url import make_url
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
jwt = JWTManager()
babel = Babel()

def create_app():
    app = Flask(__name__)

    # Get DATABASE_URL from environment or fallback to SQLite local DB for dev
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        logger.warning("DATABASE_URL not set. Using local SQLite database.")
        db_url = "sqlite:///local.db"
    else:
        # Parse and ensure driver and sslmode for PostgreSQL
        try:
            url = make_url(db_url)
            url = url.set(drivername="postgresql+psycopg2")
            # Add sslmode=require query param if not present
            if not url.query.get("sslmode"):
                url = url.set(query={**url.query, "sslmode": "require"})
            db_url = str(url)
            logger.info(f"Using DATABASE_URL: {db_url}")
        except Exception as e:
            logger.error(f"Error parsing DATABASE_URL: {e}")

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    # Set secret keys securely
    app.secret_key = os.environ.get("SESSION_SECRET") or os.urandom(24)
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "jwt-secret-string")
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    app.config["BABEL_DEFAULT_LOCALE"] = "fr"
    app.config["BABEL_DEFAULT_TIMEZONE"] = "UTC"
    app.config["LANGUAGES"] = {
        'fr': 'Français',
        'en': 'English',
        'es': 'Español',
        'pt': 'Português',
        'de': 'Deutsch',
        'it': 'Italiano',
        'ar': 'العربية'
    }

    # Apply proxy fix for correct headers behind proxy (Render)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_for=1, x_port=1, x_prefix=1)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    babel.init_app(app)

    # Google Drive credentials environment variable
    if os.path.exists('credentials.json'):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'credentials.json'
        logger.info("Google Drive credentials loaded.")
    else:
        logger.warning("credentials.json not found. Google Drive API might not work.")

    # Health check endpoint
    @app.route('/health')
    def health_check():
        from flask import jsonify
        return jsonify({'status': 'healthy', 'service': 'BENJ INSIDE', 'version': '1.0.0'}), 200

    # Main route
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')

    # Initialize DB content
    with app.app_context():
        from models import User, Department, Announcement
        from werkzeug.security import generate_password_hash

        try:
            db.create_all()
        except Exception as e:
            logger.error(f"Error during db.create_all(): {e}")

        # Default departments
        departments = ['Chantres', 'Intercesseurs', 'Régis', 'Administration', 'Jeunesse', 'Évangélisation']
        for dept_name in departments:
            if not Department.query.filter_by(nom=dept_name).first():
                db.session.add(Department(nom=dept_name))

        # Admin user
        admin = User.query.filter_by(username='Yohann').first()
        if not admin:
            admin = User(
                username='Yohann',
                email='admin@benjinside.com',
                password_hash=generate_password_hash('admin'),
                role='admin',
                langue='fr'
            )
            db.session.add(admin)

        # Default announcement
        if not Announcement.query.first():
            from datetime import date, time
            db.session.add(Announcement(
                titre="Bienvenue sur BENJ INSIDE",
                description="Plateforme de gestion chrétienne pour notre communauté. Que Dieu vous bénisse!",
                date_programme=date(2025, 7, 20),
                heure_programme=time(9, 0),
                lieu="Église BENJ INSIDE",
                statut="approuve",
                cree_par=admin.id
            ))
        db.session.commit()

    return app

app = create_app()
