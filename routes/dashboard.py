import os
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from models import User, Temoignage, Finance, Announcement, Playlist, Department, DepartmentRequest
from app import db
from datetime import datetime

dashboard_bp = Blueprint('dashboard', __name__)

def login_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vous devez être connecté pour accéder à cette page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@dashboard_bp.route('/')
@login_required
def dashboard():
    user = User.query.get(session['user_id'])
    announcements = Announcement.query.filter_by(statut='approuve').order_by(Announcement.date_creation.desc()).limit(3).all()
    
    # Get user's financial obligations
    finances = Finance.query.filter_by(user_id=user.id, paye=False).all()
    
    # Get playlist data for admin
    playlist_items = None
    pending_requests_count = 0
    if user.role == 'admin':
        playlist_items = Playlist.query.order_by(Playlist.date_ajout.desc()).limit(5).all()
        pending_requests_count = DepartmentRequest.query.filter_by(statut='en_attente').count()
    
    # Bible verse of the day (static for now)
    daily_verse = {
        'reference': 'Ésaïe 51:16',
        'text': 'Je mets mes paroles dans ta bouche, Et je te couvre de l\'ombre de ma main, Pour étendre de nouveaux cieux et fonder une nouvelle terre, Et pour dire à Sion: Tu es mon peuple!'
    }
    
    return render_template('dashboard/dashboard.html', 
                         user=user,
                         current_user=user,
                         announcements=announcements,
                         finances=finances,
                         daily_verse=daily_verse,
                         playlist_items=playlist_items,
                         pending_requests_count=pending_requests_count)

@dashboard_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    user = User.query.get(session['user_id'])
    departments = Department.query.all()
    
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']
        user.langue = request.form['langue']
        
        if request.form.get('departement_id'):
            user.departement_id = request.form['departement_id']
        
        db.session.commit()
        flash('Profil mis à jour avec succès!', 'success')
        return redirect(url_for('dashboard.profile'))
    
    return render_template('dashboard/profile.html', user=user, departments=departments)

@dashboard_bp.route('/testimonials', methods=['GET', 'POST'])
@login_required
def testimonials():
    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        contenu = request.form['contenu']
        
        if len(contenu.strip()) < 10:
            flash('Le témoignage doit contenir au moins 10 caractères', 'error')
        else:
            temoignage = Temoignage(
                user_id=user.id,
                contenu=contenu,
                statut='en_attente'
            )
            db.session.add(temoignage)
            db.session.commit()
            flash('Témoignage soumis avec succès! Il sera examiné par l\'administration.', 'success')
            return redirect(url_for('dashboard.testimonials'))
    
    # Get user's testimonials
    user_testimonials = Temoignage.query.filter_by(user_id=user.id).order_by(Temoignage.date_soumission.desc()).all()
    
    # Get approved testimonials from others
    approved_testimonials = Temoignage.query.filter(
        Temoignage.statut == 'valide',
        Temoignage.user_id != user.id
    ).order_by(Temoignage.date_soumission.desc()).limit(10).all()
    
    return render_template('dashboard/testimonials.html', 
                         user_testimonials=user_testimonials,
                         approved_testimonials=approved_testimonials)

@dashboard_bp.route('/playlist')
@login_required
def playlist():
    playlist_items = Playlist.query.order_by(Playlist.date_ajout.desc()).all()
    return render_template('dashboard/playlist.html', playlist_items=playlist_items)

@dashboard_bp.route('/chatbot')
@login_required
def chatbot():
    return render_template('dashboard/chatbot.html')
