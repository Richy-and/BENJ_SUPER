"""
Service intégré pour la gestion audio cloud avec Google Drive et base de données Render
Combine upload, stockage et gestion des liens publics
"""

import os
import logging
from werkzeug.utils import secure_filename
from datetime import datetime
from models import db, Playlist
from services.google_drive_service import google_drive_service

logger = logging.getLogger(__name__)

class CloudAudioService:
    def __init__(self):
        """Initialiser le service audio cloud"""
        self.google_drive = google_drive_service
        self.allowed_extensions = {'mp3', 'wav', 'ogg', 'm4a', 'flac', 'aac'}
    
    def is_allowed_file(self, filename):
        """Vérifier si le fichier audio est autorisé"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def upload_audio_to_cloud(self, file, title, description="", volume=0.7):
        """
        Uploader un fichier audio vers Google Drive et sauvegarder les données en base
        
        Args:
            file: FileStorage object du fichier
            title: Titre de l'audio
            description: Description optionnelle
            volume: Volume par défaut (0.0 - 1.0)
            
        Returns:
            dict: {'success': bool, 'playlist_id': int, 'message': str, 'error': str}
        """
        try:
            # Validation du fichier
            if not file or not file.filename:
                return {
                    'success': False,
                    'error': 'Aucun fichier sélectionné'
                }
            
            if not self.is_allowed_file(file.filename):
                return {
                    'success': False,
                    'error': 'Format de fichier non autorisé. Utilisez: MP3, WAV, OGG, M4A, FLAC, AAC'
                }
            
            # Préparer le nom de fichier sécurisé
            original_filename = secure_filename(file.filename)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_')
            filename = f"{timestamp}{original_filename}"
            
            # Lire les données du fichier
            file_data = file.read()
            file_size = len(file_data)
            
            # Upload vers Google Drive
            logger.info(f"Upload de {filename} vers Google Drive...")
            upload_result = self.google_drive.upload_audio_file(file_data, filename)
            
            if not upload_result['success']:
                # Si quota dépassé, fallback vers stockage local
                if upload_result.get('quota_exceeded', False):
                    logger.warning("Quota Google Drive dépassé, utilisation du stockage local...")
                    return self._save_file_locally_fallback(file_data, filename, title, description, volume)
                
                return {
                    'success': False,
                    'error': f"Erreur Google Drive: {upload_result['error']}"
                }
            
            # Créer l'entrée en base de données
            playlist_item = Playlist(
                titre=title,
                fichier_audio_url=upload_result['public_url'],
                description=description,
                volume=volume,
                is_local=False,  # Stocké sur Google Drive
                google_drive_file_id=upload_result['file_id'],
                google_drive_url=upload_result['public_url'],
                file_size=file_size,
                upload_date=datetime.utcnow()
            )
            
            db.session.add(playlist_item)
            db.session.commit()
            
            logger.info(f"Audio '{title}' ajouté avec succès (ID: {playlist_item.id})")
            return {
                'success': True,
                'playlist_id': playlist_item.id,
                'message': f"Audio '{title}' uploadé avec succès vers Google Drive",
                'error': None
            }
            
        except Exception as e:
            db.session.rollback()
            error_msg = f"Erreur lors de l'upload: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def delete_audio_from_cloud(self, playlist_id):
        """
        Supprimer un audio de Google Drive et de la base de données
        
        Args:
            playlist_id: ID de l'item dans la playlist
            
        Returns:
            dict: {'success': bool, 'message': str, 'error': str}
        """
        try:
            # Récupérer l'item de la playlist
            playlist_item = Playlist.query.get(playlist_id)
            if not playlist_item:
                return {
                    'success': False,
                    'error': 'Audio non trouvé'
                }
            
            # Si l'audio est stocké sur Google Drive
            if playlist_item.google_drive_file_id:
                logger.info(f"Suppression de Google Drive: {playlist_item.google_drive_file_id}")
                delete_result = self.google_drive.delete_audio_file(playlist_item.google_drive_file_id)
                
                if not delete_result['success']:
                    logger.warning(f"Erreur suppression Google Drive: {delete_result['error']}")
                    # On continue quand même pour supprimer de la base
            
            # Supprimer de la base de données
            title = playlist_item.titre
            db.session.delete(playlist_item)
            db.session.commit()
            
            logger.info(f"Audio '{title}' supprimé avec succès")
            return {
                'success': True,
                'message': f"Audio '{title}' supprimé avec succès",
                'error': None
            }
            
        except Exception as e:
            db.session.rollback()
            error_msg = f"Erreur lors de la suppression: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def get_audio_info(self, playlist_id):
        """
        Récupérer les informations détaillées d'un audio
        
        Args:
            playlist_id: ID de l'item dans la playlist
            
        Returns:
            dict: Informations de l'audio ou None
        """
        try:
            playlist_item = Playlist.query.get(playlist_id)
            if not playlist_item:
                return None
            
            info = {
                'id': playlist_item.id,
                'titre': playlist_item.titre,
                'description': playlist_item.description,
                'volume': playlist_item.volume,
                'fichier_audio_url': playlist_item.fichier_audio_url,
                'is_local': playlist_item.is_local,
                'date_ajout': playlist_item.date_ajout,
                'file_size': playlist_item.file_size,
                'upload_date': playlist_item.upload_date,
                'google_drive_file_id': playlist_item.google_drive_file_id,
                'google_drive_url': playlist_item.google_drive_url
            }
            
            # Si stocké sur Google Drive, récupérer infos additionnelles
            if playlist_item.google_drive_file_id:
                drive_info = self.google_drive.get_file_info(playlist_item.google_drive_file_id)
                if drive_info:
                    info['google_drive_info'] = drive_info
            
            return info
            
        except Exception as e:
            logger.error(f"Erreur récupération infos: {str(e)}")
            return None
    
    def list_all_audios(self):
        """
        Lister tous les audios de la playlist avec leurs informations
        
        Returns:
            list: Liste des audios avec leurs informations
        """
        try:
            playlist_items = Playlist.query.order_by(Playlist.date_ajout.desc()).all()
            audios = []
            
            for item in playlist_items:
                audio_info = {
                    'id': item.id,
                    'titre': item.titre,
                    'description': item.description,
                    'volume': item.volume,
                    'fichier_audio_url': item.fichier_audio_url,
                    'is_local': item.is_local,
                    'date_ajout': item.date_ajout,
                    'file_size': item.file_size,
                    'storage_type': 'Google Drive' if item.google_drive_file_id else 'Local'
                }
                audios.append(audio_info)
            
            return audios
            
        except Exception as e:
            logger.error(f"Erreur listage audios: {str(e)}")
            return []
    
    def update_audio_metadata(self, playlist_id, title=None, description=None, volume=None):
        """
        Mettre à jour les métadonnées d'un audio
        
        Args:
            playlist_id: ID de l'item
            title: Nouveau titre (optionnel)
            description: Nouvelle description (optionnelle)
            volume: Nouveau volume (optionnel)
            
        Returns:
            dict: {'success': bool, 'message': str, 'error': str}
        """
        try:
            playlist_item = Playlist.query.get(playlist_id)
            if not playlist_item:
                return {
                    'success': False,
                    'error': 'Audio non trouvé'
                }
            
            # Mettre à jour les champs modifiés
            if title is not None:
                playlist_item.titre = title
            if description is not None:
                playlist_item.description = description
            if volume is not None:
                playlist_item.volume = max(0.0, min(1.0, volume))  # Limiter entre 0 et 1
            
            db.session.commit()
            
            return {
                'success': True,
                'message': 'Métadonnées mises à jour avec succès',
                'error': None
            }
            
        except Exception as e:
            db.session.rollback()
            error_msg = f"Erreur mise à jour: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def get_storage_stats(self):
        """
        Récupérer les statistiques de stockage
        
        Returns:
            dict: Statistiques de stockage
        """
        try:
            total_audios = Playlist.query.count()
            google_drive_audios = Playlist.query.filter(Playlist.google_drive_file_id.isnot(None)).count()
            local_audios = Playlist.query.filter(Playlist.is_local == True).count()
            
            # Calculer la taille totale
            total_size = db.session.query(db.func.sum(Playlist.file_size)).scalar() or 0
            
            stats = {
                'total_audios': total_audios,
                'google_drive_audios': google_drive_audios,
                'local_audios': local_audios,
                'total_size_mb': round(total_size / (1024 * 1024), 2),
                'google_drive_service_status': self.google_drive.service is not None
            }
            
            return stats
            
        except Exception as e:
            logger.error(f"Erreur stats: {str(e)}")
            return {
                'total_audios': 0,
                'google_drive_audios': 0,
                'local_audios': 0,
                'total_size_mb': 0,
                'google_drive_service_status': False
            }

# Instance globale du service
cloud_audio_service = CloudAudioService()