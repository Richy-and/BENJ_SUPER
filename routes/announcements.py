from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename
from models import db, Announcement, User
from datetime import datetime, date, time
import json
import os
from functools import wraps

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vous devez être connecté pour accéder à cette page', 'error')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

def get_current_user():
    if 'user_id' in session:
        return User.query.get(session['user_id'])
    return None

announcements_bp = Blueprint('announcements', __name__)

# Configuration pour les uploads
UPLOAD_FOLDER = 'static/uploads/announcements'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@announcements_bp.route('/announcements')
@require_login
def announcements():
    """Page des annonces pour les ouvriers"""
    user = get_current_user()
    
    # Vérifier si l'utilisateur est ouvrier ou plus
    if user.role not in ['ouvrier', 'chef', 'admin']:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    # Récupérer les annonces créées par l'utilisateur
    mes_annonces = Announcement.query.filter_by(cree_par=user.id).order_by(Announcement.date_creation.desc()).all()
    
    # Récupérer les ouvriers pour la liste des intervenants
    ouvriers = User.query.filter(User.role.in_(['ouvrier', 'chef', 'admin'])).all()
    
    return render_template('dashboard/announcements.html', 
                         mes_annonces=mes_annonces, 
                         ouvriers=ouvriers)

@announcements_bp.route('/announcements/create', methods=['POST'])
@require_login
def create_announcement():
    """Créer une nouvelle annonce"""
    user = get_current_user()
    
    # Vérifier si l'utilisateur est ouvrier ou plus
    if user.role not in ['ouvrier', 'chef', 'admin']:
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        # Récupérer les données du formulaire
        titre = request.form.get('titre')
        description = request.form.get('description')
        date_programme = request.form.get('date_programme')
        heure_programme = request.form.get('heure_programme')
        lieu = request.form.get('lieu')
        intervenants_ids = request.form.getlist('intervenants')
        
        # Validation
        if not titre or not description or not date_programme or not heure_programme:
            flash('Tous les champs obligatoires doivent être remplis', 'error')
            return redirect(url_for('announcements.announcements'))
        
        # Traiter la photo si fournie
        photo_url = None
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and allowed_file(file.filename):
                # Créer le dossier s'il n'existe pas
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                
                # Sécuriser le nom du fichier
                filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                photo_url = f"/static/uploads/announcements/{filename}"
        
        # Convertir les dates
        date_prog = datetime.strptime(date_programme, '%Y-%m-%d').date()
        heure_prog = datetime.strptime(heure_programme, '%H:%M').time()
        
        # Créer l'annonce
        annonce = Announcement(
            titre=titre,
            description=description,
            date_programme=date_prog,
            heure_programme=heure_prog,
            lieu=lieu,
            photo_url=photo_url,
            intervenants=json.dumps(intervenants_ids) if intervenants_ids else None,
            cree_par=user.id,
            statut='en_attente' if user.role != 'admin' else 'approuve'
        )
        
        # Approuver automatiquement si admin
        if user.role == 'admin':
            annonce.approuve_par = user.id
            annonce.date_approbation = datetime.utcnow()
        
        db.session.add(annonce)
        db.session.commit()
        
        flash('Annonce créée avec succès', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la création : {str(e)}', 'error')
    
    return redirect(url_for('announcements.announcements'))

@announcements_bp.route('/announcements/edit/<int:announcement_id>', methods=['POST'])
@require_login
def edit_announcement(announcement_id):
    """Modifier une annonce"""
    user = get_current_user()
    
    annonce = Announcement.query.get_or_404(announcement_id)
    
    # Vérifier les permissions
    if annonce.cree_par != user.id and user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('announcements.announcements'))
    
    try:
        # Récupérer les données du formulaire
        annonce.titre = request.form.get('titre')
        annonce.description = request.form.get('description')
        annonce.date_programme = datetime.strptime(request.form.get('date_programme'), '%Y-%m-%d').date()
        annonce.heure_programme = datetime.strptime(request.form.get('heure_programme'), '%H:%M').time()
        annonce.lieu = request.form.get('lieu')
        
        intervenants_ids = request.form.getlist('intervenants')
        annonce.intervenants = json.dumps(intervenants_ids) if intervenants_ids else None
        
        # Traiter la nouvelle photo si fournie
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and allowed_file(file.filename):
                # Créer le dossier s'il n'existe pas
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                
                # Supprimer l'ancienne photo
                if annonce.photo_url:
                    old_filepath = os.path.join('static', annonce.photo_url.lstrip('/static/'))
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath)
                
                # Sauvegarder la nouvelle photo
                filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                annonce.photo_url = f"/static/uploads/announcements/{filename}"
        
        # Remettre en attente si modifiée par un non-admin
        if user.role != 'admin' and annonce.statut == 'approuve':
            annonce.statut = 'en_attente'
            annonce.approuve_par = None
            annonce.date_approbation = None
        
        db.session.commit()
        flash('Annonce modifiée avec succès', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la modification : {str(e)}', 'error')
    
    return redirect(url_for('announcements.announcements'))

@announcements_bp.route('/announcements/delete/<int:announcement_id>', methods=['POST'])
@require_login
def delete_announcement(announcement_id):
    """Supprimer une annonce"""
    user = get_current_user()
    
    annonce = Announcement.query.get_or_404(announcement_id)
    
    # Vérifier les permissions
    if annonce.cree_par != user.id and user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('announcements.announcements'))
    
    try:
        # Supprimer la photo associée
        if annonce.photo_url:
            filepath = os.path.join('static', annonce.photo_url.lstrip('/static/'))
            if os.path.exists(filepath):
                os.remove(filepath)
        
        db.session.delete(annonce)
        db.session.commit()
        
        flash('Annonce supprimée avec succès', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression : {str(e)}', 'error')
    
    return redirect(url_for('announcements.announcements'))

@announcements_bp.route('/admin/announcements')
@require_login
def admin_announcements():
    """Page d'administration des annonces"""
    user = get_current_user()
    
    if user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    # Récupérer toutes les annonces
    annonces = Announcement.query.order_by(Announcement.date_creation.desc()).all()
    
    # Récupérer tous les utilisateurs pour afficher les noms
    users = User.query.all()
    
    return render_template('admin/announcements_admin.html', annonces=annonces, users=users)

@announcements_bp.route('/admin/announcements/approve/<int:announcement_id>', methods=['POST'])
@require_login
def approve_announcement(announcement_id):
    """Approuver une annonce"""
    user = get_current_user()
    
    if user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        annonce = Announcement.query.get_or_404(announcement_id)
        annonce.statut = 'approuve'
        annonce.approuve_par = user.id
        annonce.date_approbation = datetime.utcnow()
        
        db.session.commit()
        flash('Annonce approuvée avec succès', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'approbation : {str(e)}', 'error')
    
    return redirect(url_for('announcements.admin_announcements'))

@announcements_bp.route('/admin/announcements/reject/<int:announcement_id>', methods=['POST'])
@require_login
def reject_announcement(announcement_id):
    """Rejeter une annonce"""
    user = get_current_user()
    
    if user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        annonce = Announcement.query.get_or_404(announcement_id)
        annonce.statut = 'rejete'
        annonce.approuve_par = user.id
        annonce.date_approbation = datetime.utcnow()
        
        db.session.commit()
        flash('Annonce rejetée', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors du rejet : {str(e)}', 'error')
    
    return redirect(url_for('announcements.admin_announcements'))

@announcements_bp.route('/admin/announcements/edit/<int:announcement_id>', methods=['POST'])
@require_login
def admin_edit_announcement(announcement_id):
    """Modifier une annonce depuis l'administration"""
    user = get_current_user()
    
    if user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        annonce = Announcement.query.get_or_404(announcement_id)
        
        # Récupérer les données du formulaire
        annonce.titre = request.form.get('titre')
        annonce.description = request.form.get('description')
        annonce.date_programme = datetime.strptime(request.form.get('date_programme'), '%Y-%m-%d').date()
        annonce.heure_programme = datetime.strptime(request.form.get('heure_programme'), '%H:%M').time()
        annonce.lieu = request.form.get('lieu')
        
        intervenants_ids = request.form.getlist('intervenants')
        annonce.intervenants = json.dumps(intervenants_ids) if intervenants_ids else None
        
        # Traiter la nouvelle photo si fournie
        if 'photo' in request.files:
            file = request.files['photo']
            if file and file.filename and allowed_file(file.filename):
                # Créer le dossier s'il n'existe pas
                os.makedirs(UPLOAD_FOLDER, exist_ok=True)
                
                # Supprimer l'ancienne photo
                if annonce.photo_url:
                    old_filepath = os.path.join('static', annonce.photo_url.lstrip('/static/'))
                    if os.path.exists(old_filepath):
                        os.remove(old_filepath)
                
                # Sauvegarder la nouvelle photo
                filename = secure_filename(f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_{file.filename}")
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)
                annonce.photo_url = f"/static/uploads/announcements/{filename}"
        
        db.session.commit()
        flash('Annonce modifiée avec succès', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la modification : {str(e)}', 'error')
    
    return redirect(url_for('announcements.admin_announcements'))