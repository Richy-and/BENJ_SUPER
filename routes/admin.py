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
    from services.cloud_audio_service import cloud_audio_service
    
    playlist_items = Playlist.query.order_by(Playlist.date_ajout.desc()).all()
    storage_stats = cloud_audio_service.get_storage_stats()
    
    return render_template('admin/playlist_admin.html', 
                         playlist_items=playlist_items,
                         storage_stats=storage_stats)

@admin_bp.route('/playlist/add', methods=['POST'])
@admin_required
def add_playlist_item():
    from services.cloud_audio_service import cloud_audio_service
    
    titre = request.form['titre']
    description = request.form.get('description', '')
    volume = float(request.form.get('volume', 0.7))
    
    # Vérifier si c'est un fichier uploadé ou une URL
    if 'fichier_audio' in request.files and request.files['fichier_audio'].filename:
        # Upload vers Google Drive
        fichier_audio = request.files['fichier_audio']
        result = cloud_audio_service.upload_audio_to_cloud(
            file=fichier_audio,
            title=titre,
            description=description,
            volume=volume
        )
        
        if result['success']:
            flash(result['message'], 'success')
        else:
            flash(f"Erreur upload: {result['error']}", 'error')
    else:
        # URL externe (méthode classique)
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
        flash('Audio URL ajouté à la playlist avec succès!', 'success')
    
    return redirect(url_for('admin.playlist_admin'))

@admin_bp.route('/playlist/delete/<int:playlist_id>', methods=['POST'])
@admin_required
def delete_playlist_item(playlist_id):
    from services.cloud_audio_service import cloud_audio_service
    
    result = cloud_audio_service.delete_audio_from_cloud(playlist_id)
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(f"Erreur suppression: {result['error']}", 'error')
    
    return redirect(url_for('admin.playlist_admin'))

@admin_bp.route('/playlist/edit/<int:playlist_id>', methods=['POST'])
@admin_required
def edit_playlist_item(playlist_id):
    from services.cloud_audio_service import cloud_audio_service
    
    titre = request.form.get('titre')
    description = request.form.get('description')
    volume = request.form.get('volume')
    
    # Convertir le volume en float si fourni
    if volume:
        volume = float(volume)
    
    result = cloud_audio_service.update_audio_metadata(
        playlist_id=playlist_id,
        title=titre,
        description=description,
        volume=volume
    )
    
    if result['success']:
        flash(result['message'], 'success')
    else:
        flash(f"Erreur mise à jour: {result['error']}", 'error')
    
    return redirect(url_for('admin.playlist_admin'))

@admin_bp.route('/playlist/info/<int:playlist_id>')
@admin_required
def playlist_item_info(playlist_id):
    from services.cloud_audio_service import cloud_audio_service
    
    audio_info = cloud_audio_service.get_audio_info(playlist_id)
    if not audio_info:
        flash('Audio non trouvé', 'error')
        return redirect(url_for('admin.playlist_admin'))
    
    return jsonify(audio_info)

@admin_bp.route('/playlist/stats')
@admin_required
def playlist_stats():
    from services.cloud_audio_service import cloud_audio_service
    
    stats = cloud_audio_service.get_storage_stats()
    return jsonify(stats)

@admin_bp.route('/announcements')
@admin_required
def announcements():
    # Séparer les annonces par statut
    pending_announcements = Announcement.query.filter_by(statut='en_attente').order_by(Announcement.date_creation.desc()).all()
    approved_announcements = Announcement.query.filter_by(statut='approuve').order_by(Announcement.date_creation.desc()).all()
    rejected_announcements = Announcement.query.filter_by(statut='rejete').order_by(Announcement.date_creation.desc()).all()
    
    return render_template('admin/announcements.html', 
                         pending_announcements=pending_announcements,
                         approved_announcements=approved_announcements,
                         rejected_announcements=rejected_announcements)

@admin_bp.route('/announcements/add', methods=['POST'])
@admin_required
def add_announcement():
    titre = request.form['titre']
    description = request.form['description']
    date_programme = request.form['date_programme']
    heure_programme = request.form['heure_programme']
    lieu = request.form.get('lieu', '')
    
    # Créer l'annonce admin directement approuvée
    announcement = Announcement(
        titre=titre,
        description=description,
        date_programme=datetime.strptime(date_programme, '%Y-%m-%d').date(),
        heure_programme=datetime.strptime(heure_programme, '%H:%M').time(),
        lieu=lieu,
        cree_par=session['user_id'],
        statut='approuve',  # Admin announcements are auto-approved
        approuve_par=session['user_id'],
        date_approbation=datetime.utcnow()
    )
    
    db.session.add(announcement)
    db.session.commit()
    
    flash('Annonce ajoutée avec succès!', 'success')
    return redirect(url_for('admin.announcements'))

@admin_bp.route('/announcements/approve/<int:announcement_id>', methods=['POST'])
@admin_required
def approve_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    announcement.statut = 'approuve'
    announcement.approuve_par = session['user_id']
    announcement.date_approbation = datetime.utcnow()
    
    db.session.commit()
    flash(f'Annonce "{announcement.titre}" approuvée avec succès!', 'success')
    return redirect(url_for('admin.announcements'))

@admin_bp.route('/announcements/reject/<int:announcement_id>', methods=['POST'])
@admin_required
def reject_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    announcement.statut = 'rejete'
    announcement.approuve_par = session['user_id']
    announcement.date_approbation = datetime.utcnow()
    
    db.session.commit()
    flash(f'Annonce "{announcement.titre}" rejetée', 'warning')
    return redirect(url_for('admin.announcements'))

@admin_bp.route('/announcements/delete/<int:announcement_id>', methods=['POST'])
@admin_required
def delete_announcement(announcement_id):
    announcement = Announcement.query.get_or_404(announcement_id)
    titre = announcement.titre
    db.session.delete(announcement)
    db.session.commit()
    
    flash(f'Annonce "{titre}" supprimée', 'success')
    return redirect(url_for('admin.announcements'))

@admin_bp.route('/members/delete/<int:user_id>', methods=['POST'])
@admin_required
def delete_user_admin(user_id):
    from models import User, Temoignage, Finance, DepartmentRequest, Announcement, Score
    
    # Récupérer l'utilisateur
    user = User.query.get(user_id)
    if not user:
        flash('Utilisateur non trouvé', 'error')
        return redirect(url_for('admin.members'))
    
    username = user.username
    
    # Vérifier que l'utilisateur n'est pas l'admin actuel
    if user_id == session['user_id']:
        flash('Vous ne pouvez pas supprimer votre propre compte', 'error')
        return redirect(url_for('admin.members'))
    
    # Vérifier que l'utilisateur n'est pas un admin
    if user.role == 'admin':
        flash('Impossible de supprimer un administrateur', 'error')
        return redirect(url_for('admin.members'))
    
    try:
        # Supprimer dans l'ordre pour éviter les violations de contraintes
        
        # 1. Mettre à NULL les références vers cet utilisateur dans d'autres tables
        db.session.execute(db.text("UPDATE department_request SET reviewed_by = NULL WHERE reviewed_by = :user_id"), {'user_id': user_id})
        db.session.execute(db.text("UPDATE announcement SET approuve_par = NULL WHERE approuve_par = :user_id"), {'user_id': user_id})
        
        # 2. Supprimer les enregistrements liés
        Score.query.filter_by(user_id=user_id).delete()
        Score.query.filter_by(chef_id=user_id).delete()
        Temoignage.query.filter_by(user_id=user_id).delete()
        Finance.query.filter_by(user_id=user_id).delete()
        DepartmentRequest.query.filter_by(user_id=user_id).delete()
        Announcement.query.filter_by(cree_par=user_id).delete()
        
        # 3. Supprimer l'utilisateur
        db.session.delete(user)
        
        # Valider la transaction
        db.session.commit()
        flash(f'Membre {username} supprimé avec succès', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression du membre: {str(e)}', 'error')
        print(f"Erreur suppression utilisateur: {e}")
        import traceback
        traceback.print_exc()
    
    return redirect(url_for('admin.members'))

@admin_bp.route('/members/edit/<int:user_id>', methods=['POST'])
@admin_required
def edit_user_admin(user_id):
    user = User.query.get_or_404(user_id)
    
    # Récupérer les données du formulaire
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    role = request.form.get('role', '').strip()
    department_id = request.form.get('departement_id')
    langue = request.form.get('langue', 'fr').strip()
    new_password = request.form.get('new_password', '').strip()
    
    # Validation des données
    if not username or not email or not role:
        flash('Tous les champs obligatoires doivent être remplis', 'error')
        return redirect(url_for('admin.members'))
    
    # Vérifier que l'username n'est pas déjà pris par un autre utilisateur
    existing_user = User.query.filter(User.username == username, User.id != user_id).first()
    if existing_user:
        flash('Ce nom d\'utilisateur est déjà pris', 'error')
        return redirect(url_for('admin.members'))
    
    # Vérifier que l'email n'est pas déjà pris par un autre utilisateur
    existing_email = User.query.filter(User.email == email, User.id != user_id).first()
    if existing_email:
        flash('Cette adresse email est déjà utilisée', 'error')
        return redirect(url_for('admin.members'))
    
    try:
        # Mettre à jour les informations de l'utilisateur
        user.username = username
        user.email = email
        user.role = role
        user.langue = langue
        
        # Mettre à jour le département si fourni
        if department_id and department_id != '':
            user.departement_id = int(department_id)
        else:
            user.departement_id = None
        
        # Mettre à jour le mot de passe si fourni
        if new_password:
            from werkzeug.security import generate_password_hash
            user.password_hash = generate_password_hash(new_password)
        
        db.session.commit()
        flash(f'Membre {username} modifié avec succès', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de la modification du membre', 'error')
        print(f"Erreur modification utilisateur: {e}")
        import traceback
        traceback.print_exc()
    
    return redirect(url_for('admin.members'))
