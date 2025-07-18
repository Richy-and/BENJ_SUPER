"""
Service Google Drive pour la gestion des fichiers audio
Permet l'upload, la suppression et la gestion des liens publics
"""

import os
import io
import json
import logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload
from google.oauth2 import service_account

logger = logging.getLogger(__name__)

class GoogleDriveService:
    def __init__(self):
        """Initialiser le service Google Drive avec les credentials"""
        self.service = None
        self.folder_id = None
        self._initialize_service()
    
    def _initialize_service(self):
        """Initialiser le service avec les credentials JSON"""
        try:
            # Chemin vers le fichier de credentials
            credentials_path = 'google_credentials.json'
            
            if not os.path.exists(credentials_path):
                logger.error("Fichier de credentials Google Drive non trouvé")
                return False
            
            # Charger les credentials
            with open(credentials_path, 'r') as f:
                credentials_info = json.load(f)
            
            # Définir les scopes nécessaires
            scopes = ['https://www.googleapis.com/auth/drive']
            
            # Créer les credentials
            credentials = service_account.Credentials.from_service_account_info(
                credentials_info, scopes=scopes
            )
            
            # Construire le service
            self.service = build('drive', 'v3', credentials=credentials)
            
            # Créer ou récupérer le dossier BENJ INSIDE Audio
            self.folder_id = self._get_or_create_folder('BENJ INSIDE Audio')
            
            logger.info("Service Google Drive initialisé avec succès")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation Google Drive: {str(e)}")
            return False
    
    def _get_or_create_folder(self, folder_name):
        """Récupérer ou créer le dossier principal pour les audios"""
        try:
            # Rechercher si le dossier existe déjà
            query = f"name='{folder_name}' and mimeType='application/vnd.google-apps.folder'"
            results = self.service.files().list(q=query).execute()
            folders = results.get('files', [])
            
            if folders:
                folder_id = folders[0]['id']
                logger.info(f"Dossier '{folder_name}' trouvé: {folder_id}")
                return folder_id
            else:
                # Créer le dossier
                folder_metadata = {
                    'name': folder_name,
                    'mimeType': 'application/vnd.google-apps.folder'
                }
                folder = self.service.files().create(body=folder_metadata).execute()
                folder_id = folder.get('id')
                
                # Rendre le dossier public (lecture seule)
                self._make_file_public(folder_id)
                
                logger.info(f"Dossier '{folder_name}' créé: {folder_id}")
                return folder_id
                
        except Exception as e:
            logger.error(f"Erreur lors de la gestion du dossier: {str(e)}")
            return None
    
    def upload_audio_file(self, file_data, filename):
        """
        Uploader un fichier audio vers Google Drive
        
        Args:
            file_data: Données binaires du fichier
            filename: Nom du fichier
            
        Returns:
            dict: {'success': bool, 'file_id': str, 'public_url': str, 'error': str}
        """
        try:
            if not self.service or not self.folder_id:
                return {
                    'success': False,
                    'error': 'Service Google Drive non initialisé'
                }
            
            # Métadonnées du fichier
            file_metadata = {
                'name': filename,
                'parents': [self.folder_id]
            }
            
            # Upload du fichier
            media = MediaIoBaseUpload(
                io.BytesIO(file_data),
                mimetype='audio/mpeg',
                resumable=True
            )
            
            file_result = self.service.files().create(
                body=file_metadata,
                media_body=media,
                fields='id'
            ).execute()
            
            file_id = file_result.get('id')
            
            # Rendre le fichier public
            public_url = self._make_file_public(file_id)
            
            if public_url:
                logger.info(f"Fichier '{filename}' uploadé avec succès: {file_id}")
                return {
                    'success': True,
                    'file_id': file_id,
                    'public_url': public_url,
                    'error': None
                }
            else:
                return {
                    'success': False,
                    'error': 'Impossible de rendre le fichier public'
                }
                
        except Exception as e:
            error_msg = f"Erreur lors de l'upload: {str(e)}"
            logger.error(error_msg)
            
            # Si c'est un problème de quota, indiquer le fallback
            if "storageQuotaExceeded" in str(e) or "quota" in str(e).lower():
                error_msg = "Quota Google Drive dépassé - fallback vers stockage local activé"
                logger.warning(error_msg)
            
            return {
                'success': False,
                'error': error_msg,
                'quota_exceeded': "quota" in str(e).lower()
            }
    
    def delete_audio_file(self, file_id):
        """
        Supprimer un fichier audio de Google Drive
        
        Args:
            file_id: ID du fichier à supprimer
            
        Returns:
            dict: {'success': bool, 'error': str}
        """
        try:
            if not self.service:
                return {
                    'success': False,
                    'error': 'Service Google Drive non initialisé'
                }
            
            # Supprimer le fichier
            self.service.files().delete(fileId=file_id).execute()
            
            logger.info(f"Fichier supprimé de Google Drive: {file_id}")
            return {
                'success': True,
                'error': None
            }
            
        except Exception as e:
            error_msg = f"Erreur lors de la suppression: {str(e)}"
            logger.error(error_msg)
            return {
                'success': False,
                'error': error_msg
            }
    
    def _make_file_public(self, file_id):
        """
        Rendre un fichier public et retourner le lien direct
        
        Args:
            file_id: ID du fichier
            
        Returns:
            str: URL publique du fichier ou None
        """
        try:
            # Permissions pour rendre public
            permission = {
                'role': 'reader',
                'type': 'anyone'
            }
            
            self.service.permissions().create(
                fileId=file_id,
                body=permission
            ).execute()
            
            # Générer le lien direct pour streaming
            public_url = f"https://drive.google.com/uc?export=download&id={file_id}"
            
            logger.info(f"Fichier rendu public: {file_id}")
            return public_url
            
        except Exception as e:
            logger.error(f"Erreur lors de la publication: {str(e)}")
            return None
    
    def get_file_info(self, file_id):
        """
        Récupérer les informations d'un fichier
        
        Args:
            file_id: ID du fichier
            
        Returns:
            dict: Informations du fichier ou None
        """
        try:
            if not self.service:
                return None
            
            file_info = self.service.files().get(
                fileId=file_id,
                fields='id,name,size,createdTime,mimeType'
            ).execute()
            
            return file_info
            
        except Exception as e:
            logger.error(f"Erreur lors de la récupération des infos: {str(e)}")
            return None
    
    def list_audio_files(self):
        """
        Lister tous les fichiers audio dans le dossier
        
        Returns:
            list: Liste des fichiers ou []
        """
        try:
            if not self.service or not self.folder_id:
                return []
            
            query = f"'{self.folder_id}' in parents and trashed=false"
            results = self.service.files().list(
                q=query,
                fields='files(id,name,size,createdTime)'
            ).execute()
            
            files = results.get('files', [])
            return files
            
        except Exception as e:
            logger.error(f"Erreur lors du listage: {str(e)}")
            return []

# Instance globale du service
google_drive_service = GoogleDriveService()