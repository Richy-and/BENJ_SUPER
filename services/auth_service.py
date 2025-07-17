from functools import wraps
from flask import session, redirect, url_for, flash
from models import User

def require_login(f):
    """Décorateur pour exiger une connexion"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vous devez être connecté pour accéder à cette page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    """Récupérer l'utilisateur connecté"""
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

def require_role(required_role):
    """Décorateur pour exiger un rôle spécifique"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Vous devez être connecté pour accéder à cette page', 'error')
                return redirect(url_for('auth.login'))
            
            user = User.query.get(session['user_id'])
            if not user or user.role != required_role:
                flash('Accès non autorisé', 'error')
                return redirect(url_for('dashboard.dashboard'))
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator