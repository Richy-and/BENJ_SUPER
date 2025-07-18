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
    # Configuration base de données - Render en priorité, puis local
    render_db_url = "postgresql://dry_moulongo_user:Mj48I1v3ZSDLOqvTBmbTBxPbTQF4SlW1@dpg-d1t4liruibrs738t5ijg-/dry_moulongo"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", render_db_url)
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
    
    # Security headers for cross-browser compatibility
    @app.after_request
    def add_security_headers(response):
        # Security headers
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'DENY'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # CORS for mobile apps
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        
        # Cache control optimized for production
        response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response.headers['Pragma'] = 'no-cache'
        response.headers['Expires'] = '0'
        
        return response

    # Health check for Render
    @app.route('/health')
    def health_check():
        from flask import jsonify
        return jsonify({
            'status': 'healthy',
            'service': 'BENJ INSIDE',
            'version': '1.0.0'
        }), 200

    # Main routes
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('index.html')
    
    # Installation page for PWA
    @app.route('/install')
    def install():
        from flask import render_template
        return render_template('install.html')
    
    # Language switching route
    @app.route('/set-language/<language_code>')
    def set_language(language_code):
        from flask import redirect, url_for, request, jsonify
        from services.translation_service import translation_service
        
        success = translation_service.set_language(language_code)
        
        # Handle AJAX requests
        if request.headers.get('Content-Type') == 'application/json' or request.is_json:
            return jsonify({
                'success': success,
                'language': language_code,
                'message': translation_service.translate('language_changed', language_code)
            })
        
        # Handle regular requests
        return redirect(request.referrer or url_for('index'))
    
    # API route for translations
    @app.route('/api/translations')
    def get_translations():
        from flask import jsonify, request
        from services.translation_service import translation_service
        
        language = request.args.get('language', translation_service.get_current_language())
        return jsonify(translation_service.get_all_translations(language))
    
    # PWA Service Worker route
    @app.route('/sw.js')
    def service_worker():
        from flask import send_from_directory
        return send_from_directory('static/js', 'sw.js', mimetype='application/javascript')
    
    # PWA Installation page
    @app.route('/install')
    def pwa_install():
        from flask import render_template
        return render_template('pwa_install.html')
    
    # Mobile test endpoint
    @app.route('/mobile-test')
    def mobile_test():
        from flask import request, jsonify
        return jsonify({
            'status': 'OK',
            'message': 'Mobile access working',
            'user_agent': request.headers.get('User-Agent', 'Unknown'),
            'remote_addr': request.remote_addr,
            'host': request.host,
            'url': request.url
        })
    
    with app.app_context():
        from models import User, Department, Announcement
        from werkzeug.security import generate_password_hash
        
        db.create_all()
        
        # Create default departments
        departments = ['Chantres', 'Intercesseurs', 'Régis', 'Administration', 'Jeunesse', 'Évangélisation']
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
            from datetime import date, time
            welcome_announcement = Announcement(
                titre="Bienvenue sur BENJ INSIDE",
                description="Plateforme de gestion chrétienne pour notre communauté. Que Dieu vous bénisse!",
                date_programme=date(2025, 7, 20),
                heure_programme=time(9, 0),
                lieu="Église BENJ INSIDE",
                statut="approuve",
                cree_par=admin.id  # Admin user
            )
            db.session.add(welcome_announcement)
        
        db.session.commit()
    
    return app

app = create_app()
