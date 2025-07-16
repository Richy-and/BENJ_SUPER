from datetime import datetime
from app import db
from flask_sqlalchemy import SQLAlchemy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='membre')  # admin, chef, ouvrier, membre
    departement_id = db.Column(db.Integer, db.ForeignKey('department.id'), nullable=True)
    langue = db.Column(db.String(10), default='fr')
    score = db.Column(db.Float, default=0.0)
    date_inscription = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    departement = db.relationship('Department', backref='users')
    temoignages = db.relationship('Temoignage', backref='user', lazy=True)
    finances = db.relationship('Finance', backref='user', lazy=True)

class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), unique=True, nullable=False)

class Temoignage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    statut = db.Column(db.String(20), default='en_attente')  # en_attente, valide, rejete
    date_soumission = db.Column(db.DateTime, default=datetime.utcnow)

class Finance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    montant = db.Column(db.Float, nullable=False)
    type = db.Column(db.String(20), nullable=False)  # cotisation, dette
    deadline = db.Column(db.DateTime, nullable=True)
    paye = db.Column(db.Boolean, default=False)
    date_creation = db.Column(db.DateTime, default=datetime.utcnow)

class Announcement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    contenu = db.Column(db.Text, nullable=False)
    date_publication = db.Column(db.DateTime, default=datetime.utcnow)

class Playlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200), nullable=False)
    fichier_audio_url = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date_ajout = db.Column(db.DateTime, default=datetime.utcnow)

class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    chef_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    score = db.Column(db.Float, nullable=False)
    commentaire = db.Column(db.Text, nullable=True)
    date_attribution = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', foreign_keys=[user_id], backref='scores_recus')
    chef = db.relationship('User', foreign_keys=[chef_id], backref='scores_donnes')
