from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from app import db
from models import DepartmentRequest, User, Department
from sqlalchemy import func
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
    demandes = DepartmentRequest.query.join(User).join(Department).order_by(
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
    
    # Statistiques par département
    stats_par_departement = db.session.query(
        Department.nom,
        func.count(DepartmentRequest.id).label('total'),
        func.sum(func.case([(DepartmentRequest.statut == 'en_attente', 1)], else_=0)).label('en_attente'),
        func.sum(func.case([(DepartmentRequest.statut == 'approuve', 1)], else_=0)).label('approuvees'),
        func.sum(func.case([(DepartmentRequest.statut == 'rejete', 1)], else_=0)).label('rejetees')
    ).join(DepartmentRequest).group_by(Department.nom).all()
    
    # Statistiques par rôle
    stats_par_role = db.session.query(
        DepartmentRequest.role_requested.label('role'),
        func.count(DepartmentRequest.id).label('total'),
        func.sum(func.case([(DepartmentRequest.statut == 'approuve', 1)], else_=0)).label('approuvees')
    ).group_by(DepartmentRequest.role_requested).all()
    
    # Calculer le taux d'approbation par rôle
    for stat in stats_par_role:
        if stat.total > 0:
            stat.taux_approbation = round((stat.approuvees / stat.total) * 100, 1)
        else:
            stat.taux_approbation = 0
    
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
    mes_demandes = DepartmentRequest.query.filter_by(user_id=user.id).join(Department).order_by(
        DepartmentRequest.created_at.desc()
    ).all()
    
    return render_template('dashboard/my_department_requests.html', mes_demandes=mes_demandes)

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