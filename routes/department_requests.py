from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from app import db
from models import DepartmentRequest, User, Department
from sqlalchemy import func, case
from services.auth_service import require_login, get_current_user

department_requests_bp = Blueprint('department_requests', __name__)

@department_requests_bp.route('/admin/department-requests')
@require_login
def admin_department_requests():
    """Page d'administration des demandes de département"""
    user = get_current_user()
    
    if user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    # Récupérer toutes les demandes avec les informations nécessaires
    demandes = DepartmentRequest.query.order_by(
        DepartmentRequest.created_at.desc()
    ).all()
    
    return render_template('admin/department_requests_admin.html', demandes=demandes)

@department_requests_bp.route('/admin/candidature-stats')
@require_login
def candidature_stats():
    """Page des statistiques des candidatures"""
    user = get_current_user()
    
    if user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    # Statistiques générales
    total_candidatures = DepartmentRequest.query.count()
    candidatures_en_attente = DepartmentRequest.query.filter_by(statut='en_attente').count()
    candidatures_approuvees = DepartmentRequest.query.filter_by(statut='approuve').count()
    candidatures_rejetees = DepartmentRequest.query.filter_by(statut='rejete').count()
    
    # Taux d'approbation
    taux_approbation = 0
    if total_candidatures > 0:
        taux_approbation = round((candidatures_approuvees / total_candidatures) * 100, 1)
    
    # Statistiques par département - approche simplifiée
    departments = Department.query.all()
    stats_par_departement = []
    
    for dept in departments:
        dept_requests = DepartmentRequest.query.filter_by(department_id=dept.id).all()
        total = len(dept_requests)
        en_attente = len([r for r in dept_requests if r.statut == 'en_attente'])
        approuvees = len([r for r in dept_requests if r.statut == 'approuve'])
        rejetees = len([r for r in dept_requests if r.statut == 'rejete'])
        
        stats_par_departement.append({
            'nom': dept.nom,
            'total': total,
            'en_attente': en_attente,
            'approuvees': approuvees,
            'rejetees': rejetees
        })
    
    # Statistiques par rôle - approche simplifiée
    roles = ['ouvrier', 'chef', 'chantres', 'intercesseurs', 'régis', 'chef_chantres', 'chef_intercesseurs', 'chef_régis']
    stats_par_role = []
    
    for role in roles:
        role_requests = DepartmentRequest.query.filter_by(role_requested=role).all()
        total = len(role_requests)
        approuvees = len([r for r in role_requests if r.statut == 'approuve'])
        
        taux_approbation = 0
        if total > 0:
            taux_approbation = round((approuvees / total) * 100, 1)
        
        if total > 0:  # Seulement inclure les rôles qui ont des demandes
            stats_par_role.append({
                'role': role,
                'total': total,
                'approuvees': approuvees,
                'taux_approbation': taux_approbation
            })
    
    return render_template('admin/candidature_stats.html',
                         total_candidatures=total_candidatures,
                         candidatures_en_attente=candidatures_en_attente,
                         candidatures_approuvees=candidatures_approuvees,
                         candidatures_rejetees=candidatures_rejetees,
                         taux_approbation=taux_approbation,
                         stats_par_departement=stats_par_departement,
                         stats_par_role=stats_par_role)

@department_requests_bp.route('/admin/department-requests/approve/<int:request_id>', methods=['POST'])
@require_login
def approve_department_request(request_id):
    """Approuver une demande de département"""
    user = get_current_user()
    
    if user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        demande = DepartmentRequest.query.get_or_404(request_id)
        admin_notes = request.form.get('admin_notes', '')
        
        # Mettre à jour la demande
        demande.statut = 'approuve'
        demande.reviewed_at = datetime.utcnow()
        demande.reviewed_by = user.id
        demande.admin_notes = admin_notes
        
        # Mettre à jour le profil de l'utilisateur
        demande.user.role = demande.role_requested
        demande.user.departement_id = demande.department_id
        
        db.session.commit()
        flash(f'Demande de {demande.user.username} approuvée avec succès', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de l\'approbation : {str(e)}', 'error')
    
    return redirect(url_for('department_requests.admin_department_requests'))

@department_requests_bp.route('/admin/department-requests/reject/<int:request_id>', methods=['POST'])
@require_login
def reject_department_request(request_id):
    """Rejeter une demande de département"""
    user = get_current_user()
    
    if user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        demande = DepartmentRequest.query.get_or_404(request_id)
        admin_notes = request.form.get('admin_notes', '')
        
        # Mettre à jour la demande
        demande.statut = 'rejete'
        demande.reviewed_at = datetime.utcnow()
        demande.reviewed_by = user.id
        demande.admin_notes = admin_notes
        
        db.session.commit()
        flash(f'Demande de {demande.user.username} rejetée', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors du rejet : {str(e)}', 'error')
    
    return redirect(url_for('department_requests.admin_department_requests'))

@department_requests_bp.route('/admin/department-requests/delete/<int:request_id>', methods=['POST'])
@require_login
def delete_department_request(request_id):
    """Supprimer une demande de département"""
    user = get_current_user()
    
    if user.role != 'admin':
        flash('Accès non autorisé', 'error')
        return redirect(url_for('dashboard.dashboard'))
    
    try:
        demande = DepartmentRequest.query.get_or_404(request_id)
        username = demande.user.username
        
        db.session.delete(demande)
        db.session.commit()
        flash(f'Demande de {username} supprimée définitivement', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'Erreur lors de la suppression : {str(e)}', 'error')
    
    return redirect(url_for('department_requests.admin_department_requests'))

@department_requests_bp.route('/my-requests')
@require_login
def my_department_requests():
    """Voir mes demandes de département"""
    user = get_current_user()
    
    # Récupérer toutes les demandes de l'utilisateur
    mes_demandes = DepartmentRequest.query.filter_by(user_id=user.id).order_by(
        DepartmentRequest.created_at.desc()
    ).all()
    
    return render_template('dashboard/my_department_requests.html', mes_demandes=mes_demandes)

@department_requests_bp.route('/candidatures')
@require_login
def department_candidatures():
    """Page principale des candidatures pour les membres"""
    user = get_current_user()
    
    # Récupérer les départements disponibles
    departments = Department.query.all()
    
    # Récupérer les candidatures existantes de l'utilisateur
    mes_candidatures = DepartmentRequest.query.filter_by(user_id=user.id).order_by(
        DepartmentRequest.created_at.desc()
    ).all()
    
    return render_template('dashboard/department_candidature.html', 
                         departments=departments, 
                         mes_candidatures=mes_candidatures)

@department_requests_bp.route('/department-request', methods=['GET', 'POST'])
@require_login
def create_department_request():
    """Créer une demande de département"""
    user = get_current_user()
    
    if request.method == 'POST':
        try:
            # Vérifier si l'utilisateur a déjà une demande en attente
            existing_request = DepartmentRequest.query.filter_by(
                user_id=user.id,
                statut='en_attente'
            ).first()
            
            if existing_request:
                flash('Vous avez déjà une demande en attente', 'warning')
                return redirect(url_for('dashboard.dashboard'))
            
            department_id = request.form.get('department_id')
            role_requested = request.form.get('role_requested')
            motivation = request.form.get('motivation')
            
            # Créer la demande
            demande = DepartmentRequest(
                user_id=user.id,
                department_id=department_id,
                role_requested=role_requested,
                motivation=motivation
            )
            
            db.session.add(demande)
            db.session.commit()
            
            flash('Votre demande a été soumise avec succès', 'success')
            return redirect(url_for('dashboard.dashboard'))
            
        except Exception as e:
            db.session.rollback()
            flash(f'Erreur lors de la soumission : {str(e)}', 'error')
    
    # Récupérer les départements disponibles
    departments = Department.query.all()
    return render_template('dashboard/department_request.html', departments=departments)