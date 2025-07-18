import os
import logging
import ssl
import psycopg2
from datetime import timedelta

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_babel import Babel
from sqlalchemy.orm import DeclarativeBase
from werkzeug.middleware.proxy_fix import ProxyFix

# Configure logging
logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
jwt = JWTManager()
babel = Babel()

def create_app():
    app = Flask(__name__)

    # Force SSL for PostgreSQL on Render
    os.environ['PGSSLMODE'] = 'require'

    # Configuration base de données - Render en priorité, puis local
    db_url = os.environ.get("DATABASE_URL")
    if not db_url:
        logging.warning("DATABASE_URL not set. Using local SQLite database.")
        db_url = "sqlite:///local.db"

    app.config["SQLALCHEMY_DATABASE_URI"] = db_url
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }

    app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")
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

    # Apply proxy fix for production - Essential for external access on Render
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_for=1, x_port=1, x_prefix=1)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    babel.init_app(app)

    # Initialize translation service
    from services.translation_service import register_template_context
    register_template_context(app)

    # Add custom Jinja filters
    import json
    @app.template_filter('from_json')
    def from_json_filter(value):
        if value:
            return json.loads(value)
        return []

    # Register blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.admin import admin_bp
    from routes.chef import chef_bp
    from routes.chatbot import chatbot_bp
    from routes.announcements import announcements_bp
    from routes.department_requests import department_requests_bp
    from routes.finances import finances_bp

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(department_requests_bp, url_prefix='/department-requests')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(chef_bp, url_prefix='/chef')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    app.register_blueprint(announcements_bp)
    app.register_blueprint(finances_bp)

    # Security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        return response

    # Health check
    @app.route('/health')
    def health_check():
        from flask import jsonify
        return jsonify({'status': 'healthy', 'service': 'BENJ INSIDE', 'version': '1.0.0'}), 200

    # Main routes
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')

    with app.app_context():
        from models import User, Department, Announcement
        from werkzeug.security import generate_password_hash

        db.create_all()

        # Create default departments
        departments = ['Chantres', 'Intercesseurs', 'Régis', 'Administration', 'Jeunesse', 'Évangélisation']
        for dept_name in departments:
            if not Department.query.filter_by(nom=dept_name).first():
                db.session.add(Department(nom=dept_name))

        # Create admin user
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

        # Create default announcement
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




