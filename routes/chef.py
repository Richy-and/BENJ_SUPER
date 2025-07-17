from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models import User, Score, Department
from app import db

chef_bp = Blueprint('chef', __name__)

def chef_required(f):
    def wrapper(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vous devez être connecté pour accéder à cette page', 'error')
            return redirect(url_for('auth.login'))
        
        user_role = session.get('user_role')
        # Autoriser tous les rôles de chef et admin
        chef_roles = ['chef', 'admin', 'chef_chantres', 'chef_intercesseurs', 'chef_régis']
        if user_role not in chef_roles:
            flash('Accès refusé. Droits de chef requis.', 'error')
            return redirect(url_for('dashboard.dashboard'))
        
        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper

@chef_bp.route('/workers')
@chef_required
def workers():
    chef = User.query.get(session['user_id'])
    
    if chef.role == 'admin':
        # Admin can see all workers
        workers = User.query.filter_by(role='ouvrier').all()
    else:
        # Chef can only see workers from their department
        # Support all types of chef roles
        workers = User.query.filter(
            User.role == 'ouvrier',
            User.departement_id == chef.departement_id
        ).all()
    
    # Get latest scores for each worker
    worker_scores = {}
    for worker in workers:
        latest_score = Score.query.filter_by(user_id=worker.id).order_by(Score.date_attribution.desc()).first()
        worker_scores[worker.id] = latest_score
    
    return render_template('chef/workers.html', workers=workers, worker_scores=worker_scores, chef=chef)

@chef_bp.route('/score/<int:worker_id>', methods=['POST'])
@chef_required
def assign_score(worker_id):
    chef = User.query.get(session['user_id'])
    worker = User.query.get_or_404(worker_id)
    
    # Verify chef can score this worker
    if chef.role != 'admin' and worker.departement_id != chef.departement_id:
        flash('Vous ne pouvez noter que les ouvriers de votre département', 'error')
        return redirect(url_for('chef.workers'))
    
    if worker.role != 'ouvrier':
        flash('Vous ne pouvez noter que les ouvriers', 'error')
        return redirect(url_for('chef.workers'))
    
    try:
        score_value = float(request.form.get('score', 0))
        commentaire = request.form.get('commentaire', '').strip()
        
        # Validate score range
        if not (0 <= score_value <= 20):
            flash('La note doit être entre 0 et 20', 'error')
            return redirect(url_for('chef.workers'))
        
        # Create new score record
        score = Score(
            user_id=worker_id,
            chef_id=chef.id,
            score=score_value,
            commentaire=commentaire
        )
        
        # Update user's current score
        worker.score = score_value
        
        db.session.add(score)
        db.session.commit()
        
        flash(f'Note de {score_value}/20 attribuée à {worker.username} avec succès!', 'success')
        
    except (ValueError, TypeError) as e:
        flash('Erreur lors de la saisie de la note. Veuillez réessayer.', 'error')
        print(f"Erreur scoring: {e}")
    except Exception as e:
        db.session.rollback()
        flash('Erreur lors de l\'attribution de la note. Veuillez réessayer.', 'error')
        print(f"Erreur DB: {e}")
    
    return redirect(url_for('chef.workers'))

@chef_bp.route('/score_history/<int:worker_id>')
@chef_required
def score_history(worker_id):
    chef = User.query.get(session['user_id'])
    worker = User.query.get_or_404(worker_id)
    
    # Verify chef can view this worker's scores
    if chef.role != 'admin' and worker.departement_id != chef.departement_id:
        flash('Accès refusé', 'error')
        return redirect(url_for('chef.workers'))
    
    scores = Score.query.filter_by(user_id=worker_id).order_by(Score.date_attribution.desc()).all()
    
    return render_template('chef/score_history.html', worker=worker, scores=scores)
