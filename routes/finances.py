from flask import Blueprint, render_template, request, redirect, url_for, flash
from app import db
from models import Finance, User
from services.auth_service import require_login, get_current_user

finances_bp = Blueprint('finances', __name__)

@finances_bp.route('/finances')
@require_login
def finances():
    """Page des finances pour les membres"""
    user = get_current_user()
    
    # Récupérer toutes les transactions de l'utilisateur
    transactions = Finance.query.filter_by(user_id=user.id).order_by(Finance.date_creation.desc()).all()
    
    # Calculer les totaux
    total_du = 0
    total_cotisations = 0
    total_dettes = 0
    
    for transaction in transactions:
        if not transaction.paye:
            total_du += transaction.montant
            
            if transaction.type == 'cotisation':
                total_cotisations += transaction.montant
            elif transaction.type == 'dette':
                total_dettes += transaction.montant
    
    return render_template('finances.html', 
                         transactions=transactions,
                         total_du=total_du,
                         total_cotisations=total_cotisations,
                         total_dettes=total_dettes)