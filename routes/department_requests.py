from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from app import db
from models import DepartmentRequest, User, Department
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