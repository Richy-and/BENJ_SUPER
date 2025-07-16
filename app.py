import os
import logging
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
    
    # Configuration
    app.secret_key = os.environ.get("SESSION_SECRET", "your-secret-key-here")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "postgresql://localhost/benj_inside")
    app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
        "pool_recycle": 300,
        "pool_pre_ping": True,
    }
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
    
    # Apply proxy fix for production
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    babel.init_app(app)
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.dashboard import dashboard_bp
    from routes.admin import admin_bp
    from routes.chef import chef_bp
    from routes.chatbot import chatbot_bp
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(chef_bp, url_prefix='/chef')
    app.register_blueprint(chatbot_bp, url_prefix='/chatbot')
    
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
        departments = ['Chantres', 'Intercesseurs', 'Régis']
        for dept_name in departments:
            if not Department.query.filter_by(nom=dept_name).first():
                dept = Department(nom=dept_name)
                db.session.add(dept)
        
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
            welcome_announcement = Announcement(
                titre="Bienvenue sur BENJ INSIDE",
                contenu="Plateforme de gestion chrétienne pour notre communauté. Que Dieu vous bénisse!"
            )
            db.session.add(welcome_announcement)
        
        db.session.commit()
    
    return app

app = create_app()
