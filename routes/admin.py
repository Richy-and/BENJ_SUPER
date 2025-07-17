from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User, Temoignage, Finance, Announcement, Playlist, Department
from app import db
from datetime import datetime
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vous devez être connecté pour accéder à cette page', 'error')
            return redirect(url_for('auth.login'))
        
        if session.get('user_role') != 'admin':
            flash('Accès refusé. Droits administrateur requis.', 'error')
            return redirect(url_for('dashboard.dashboard'))
        
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@admin_bp.route('/members')
@admin_required
def members():
    users = User.query.all()
    departments = Department.query.all()
    return render_template('admin/members.html', users=users, departments=departments)

@admin_bp.route('/members/add', methods=['POST'])
@admin_required
def add_member():
    from werkzeug.security import generate_password_hash
    
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    role = request.form['role']
    departement_id = request.form.get('departement_id')
    langue = request.form.get('langue', 'fr')
    
    # Vérifier si l'utilisateur existe déjà
    if User.query.filter_by(username=username).first():
        flash('Ce nom d\'utilisateur existe déjà', 'error')
        return redirect(url_for('admin.members'))
    
    if User.query.filter_by(email=email).first():
        flash('Cette adresse email est déjà utilisée', 'error')
        return redirect(url_for('admin.members'))
    
    # Créer le nouvel utilisateur
    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
        role=role,
        departement_id=departement_id if departement_id else None,
        langue=langue
    )
    
    db.session.add(user)
    db.session.commit()
    
    flash(f'Membre {username} ajouté avec succès!', 'success')
    return redirect(url_for('admin.members'))

@admin_bp.route('/members/update/<int:user_id>', methods=['POST'])
@admin_required
def update_member(user_id):
    user = User.query.get_or_404(user_id)
    
    user.username = request.form['username']
    user.email = request.form['email']
    user.role = request.form['role']
    user.langue = request.form.get('langue', 'fr')
    
    if request.form.get('departement_id'):
        user.departement_id = request.form['departement_id']
    else:
        user.departement_id = None
    
    # Mettre à jour le mot de passe si fourni
    if request.form.get('password'):
        from werkzeug.security import generate_password_hash
        user.password_hash = generate_password_hash(request.form['password'])
    
    db.session.commit()
    flash(f'Utilisateur {user.username} mis à jour avec succès!', 'success')
    return redirect(url_for('admin.members'))

@admin_bp.route('/members/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_member(user_id):
    user = User.query.get_or_404(user_id)
    
    if user.role == 'admin':
        flash('Impossible de supprimer un administrateur', 'error')
        return redirect(url_for('admin.members'))
    
    # Delete related records
    Temoignage.query.filter_by(user_id=user_id).delete()
    Finance.query.filter_by(user_id=user_id).delete()
    
    db.session.delete(user)
    db.session.commit()
    
    flash(f'Utilisateur {user.username} supprimé avec succès!', 'success')
    return redirect(url_for('admin.members'))

@admin_bp.route('/finances')
@admin_required
def finances():
    finances = Finance.query.join(User).order_by(Finance.date_creation.desc()).all()
    users = User.query.all()
    return render_template('admin/finances.html', finances=finances, users=users)

@admin_bp.route('/finances/add', methods=['POST'])
@admin_required
def add_finance():
    user_id = request.form['user_id']
    montant = float(request.form['montant'])
    type_finance = request.form['type']
    deadline_str = request.form.get('deadline')
    
    deadline = None
    if deadline_str:
        deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
    
    finance = Finance(
        user_id=user_id,
        montant=montant,
        type=type_finance,
        deadline=deadline
    )
    
    db.session.add(finance)
    db.session.commit()
    
    flash('Transaction financière ajoutée avec succès!', 'success')
    return redirect(url_for('admin.finances'))

@admin_bp.route('/finances/toggle/<int:finance_id>', methods=['POST'])
@admin_required
def toggle_payment(finance_id):
    finance = Finance.query.get_or_404(finance_id)
    finance.paye = not finance.paye
    db.session.commit()
    
    status = 'payée' if finance.paye else 'non payée'
    flash(f'Transaction marquée comme {status}', 'success')
    return redirect(url_for('admin.finances'))

@admin_bp.route('/finances/update/<int:finance_id>', methods=['POST'])
@admin_required
def update_finance(finance_id):
    finance = Finance.query.get_or_404(finance_id)
    
    finance.user_id = request.form['user_id']
    finance.montant = float(request.form['montant'])
    finance.type = request.form['type']
    
    deadline_str = request.form.get('deadline')
    if deadline_str:
        finance.deadline = datetime.strptime(deadline_str, '%Y-%m-%d')
    else:
        finance.deadline = None
    
    db.session.commit()
    flash('Transaction mise à jour avec succès!', 'success')
    return redirect(url_for('admin.finances'))

@admin_bp.route('/finances/delete/<int:finance_id>', methods=['POST'])
@admin_required
def delete_finance(finance_id):
    finance = Finance.query.get_or_404(finance_id)
    db.session.delete(finance)
    db.session.commit()
    
    flash('Transaction supprimée avec succès!', 'success')
    return redirect(url_for('admin.finances'))

@admin_bp.route('/testimonials')
@admin_required
def testimonials_admin():
    testimonials = Temoignage.query.join(User).order_by(Temoignage.date_soumission.desc()).all()
    return render_template('admin/testimonials_admin.html', testimonials=testimonials)

@admin_bp.route('/testimonials/update/<int:testimonial_id>', methods=['POST'])
@admin_required
def update_testimonial(testimonial_id):
    testimonial = Temoignage.query.get_or_404(testimonial_id)
    action = request.form['action']
    
    if action == 'approve':
        testimonial.statut = 'valide'
        flash('Témoignage approuvé avec succès!', 'success')
    elif action == 'reject':
        testimonial.statut = 'rejete'
        flash('Témoignage rejeté', 'info')
    
    db.session.commit()
    return redirect(url_for('admin.testimonials_admin'))

@admin_bp.route('/playlist')
@admin_required
def playlist_admin():
    playlist_items = Playlist.query.order_by(Playlist.date_ajout.desc()).all()
    return render_template('admin/playlist_admin.html', playlist_items=playlist_items)

@admin_bp.route('/playlist/add', methods=['POST'])
@admin_required
def add_playlist_item():
    titre = request.form['titre']
    description = request.form.get('description', '')
    volume = float(request.form.get('volume', 0.7))
    
    # Vérifier si c'est un fichier local ou une URL
    if 'fichier_audio' in request.files and request.files['fichier_audio'].filename:
        # Fichier local uploadé
        fichier_audio = request.files['fichier_audio']
        if fichier_audio and fichier_audio.filename:
            # Sauvegarder le fichier localement
            filename = secure_filename(fichier_audio.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = timestamp + filename
            filepath = os.path.join('static/audio', filename)
            fichier_audio.save(filepath)
            
            playlist_item = Playlist(
                titre=titre,
                fichier_audio_url=f'/static/audio/{filename}',
                description=description,
                volume=volume,
                is_local=True
            )
    else:
        # URL externe
        fichier_audio_url = request.form['fichier_audio_url']
        playlist_item = Playlist(
            titre=titre,
            fichier_audio_url=fichier_audio_url,
            description=description,
            volume=volume,
            is_local=False
        )
    
    db.session.add(playlist_item)
    db.session.commit()
    
    flash('Audio ajouté à la playlist avec succès!', 'success')
    return redirect(url_for('admin.playlist_admin'))

@admin_bp.route('/playlist/delete/<int:playlist_id>', methods=['POST'])
@admin_required
def delete_playlist_item(playlist_id):
    playlist_item = Playlist.query.get_or_404(playlist_id)
    db.session.delete(playlist_item)
    db.session.commit()
    
    flash('Audio supprimé de la playlist', 'success')
    return redirect(url_for('admin.playlist_admin'))

@admin_bp.route('/announcements')
@admin_required
def announcements():
    announcements = Announcement.query.order_by(Announcement.date_publication.desc()).all()
    return render_template('admin/announcements.html', announcements=announcements)

@admin_bp.route('/announcements/add', methods=['POST'])
@admin_required
def add_announcement():
    titre = request.form['titre']
    contenu = request.form['contenu']
    
    announcement = Announcement(
        titre=titre,
        contenu=contenu
    )
    
    db.session.add(announcement)
    db.session.commit()
    
    flash('Annonce ajoutée avec succès!', 'success')
    return redirect(url_for('admin.announcements'))

@admin_bp.route('/announcements/delete/<int:announcement_id>', methods=['POST'])
@admin_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    db.session.delete(announcement)
    db.session.commit()
    
    flash('Annonce supprimée', 'success')
    return redirect(url_for('admin.announcements'))

@admin_bp.route('/members/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user_admin(user_id):
    from models import Score, Temoignage, Finance, Announcement, DepartmentRequest
    
    user = User.query.get_or_404(user_id)
    
    # Vérifier que l'utilisateur n'est pas l'admin actuel
    if user.id == session['user_id']:
        flash('Vous ne pouvez pas supprimer votre propre compte', 'error')
        return redirect(url_for('admin.members'))
    
    try:
        # Supprimer d'abord tous les scores associés (reçus et donnés)
        scores_user = Score.query.filter_by(user_id=user_id).all()
        for score in scores_user:
            db.session.delete(score)
        
        scores_chef = Score.query.filter_by(chef_id=user_id).all()
        for score in scores_chef:
            db.session.delete(score)
        
        # Supprimer tous les témoignages associés
        temoignages = Temoignage.query.filter_by(user_id=user_id).all()
        for temoignage in temoignages:
            db.session.delete(temoignage)
        
        # Supprimer toutes les finances associées
        finances = Finance.query.filter_by(user_id=user_id).all()
        for finance in finances:
            db.session.delete(finance)
        
        # Supprimer toutes les demandes de département associées
        dept_requests_user = DepartmentRequest.query.filter_by(user_id=user_id).all()
        for request in dept_requests_user:
            db.session.delete(request)
            
        dept_requests_reviewer = DepartmentRequest.query.filter_by(reviewed_by=user_id).all()
        for request in dept_requests_reviewer:
            request.reviewed_by = None
            request.admin_notes = f"Révisé par utilisateur supprimé - {request.admin_notes or ''}"
        
        # Supprimer les annonces créées par cet utilisateur
        announcements_created = Announcement.query.filter_by(cree_par=user_id).all()
        for announcement in announcements_created:
            db.session.delete(announcement)
        
        # Mettre à jour les annonces approuvées par cet utilisateur (remettre à null)
        announcements_approved = Announcement.query.filter_by(approuve_par=user_id).all()
        for announcement in announcements_approved:
            announcement.approuve_par = None
            announcement.date_approbation = None
        
        # Commit toutes les modifications des relations avant de supprimer l'utilisateur
        db.session.commit()
        
        # Supprimer l'utilisateur
        db.session.delete(user)
        db.session.commit()
        
        flash(f'Membre {user.username} supprimé avec succès', 'success')
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la suppression du membre', 'error')
        print(f"Erreur suppression utilisateur: {e}")
        import traceback
        traceback.print_exc()
    
    return redirect(url_for('admin.members'))
