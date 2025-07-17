"""
Translation service for BENJ INSIDE multilingual support
Handles language switching and provides translations for UI and chatbot
"""

import json
import os
from flask import session, request, g
from functools import wraps

class TranslationService:
    def __init__(self):
        self.translations = {}
        self.default_language = 'fr'
        self.supported_languages = ['fr', 'en', 'es', 'pt', 'de', 'it', 'ar']
        self.load_translations()
    
    def load_translations(self):
        """Load translations from JSON file"""
        try:
            with open('translations.json', 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            print("Warning: translations.json not found. Using default translations.")
            self.translations = self._get_default_translations()
    
    def _get_default_translations(self):
        """Fallback translations if file is missing"""
        return {
            'fr': {
                'app_name': 'BENJ INSIDE',
                'welcome': 'Bienvenue',
                'dashboard': 'Tableau de bord',
                'profile': 'Mon Profil',
                'login': 'Se connecter',
                'logout': 'Déconnexion'
            },
            'en': {
                'app_name': 'BENJ INSIDE',
                'welcome': 'Welcome',
                'dashboard': 'Dashboard',
                'profile': 'My Profile',
                'login': 'Login',
                'logout': 'Logout'
            }
        }
    
    def get_current_language(self):
        """Get current user's language preference"""
        # Check if user is logged in and has language preference
        if 'user_id' in session:
            from models import User
            user = User.query.get(session['user_id'])
            if user and user.langue in self.supported_languages:
                return user.langue
        
        # Fallback to session language
        if 'language' in session:
            return session['language']
        
        # Auto-detect from browser headers
        if request and hasattr(request, 'accept_languages'):
            browser_lang = request.accept_languages.best_match(self.supported_languages)
            if browser_lang:
                return browser_lang
        
        return self.default_language
    
    def set_language(self, language_code):
        """Set current language"""
        if language_code in self.supported_languages:
            session['language'] = language_code
            
            # Update user's language preference if logged in
            if 'user_id' in session:
                from models import User
                from app import db
                user = User.query.get(session['user_id'])
                if user:
                    user.langue = language_code
                    db.session.commit()
            
            return True
        return False
    
    def translate(self, key, language=None):
        """Get translation for a key"""
        if language is None:
            language = self.get_current_language()
        
        if language not in self.translations:
            language = self.default_language
        
        return self.translations[language].get(key, key)
    
    def get_all_translations(self, language=None):
        """Get all translations for a language"""
        if language is None:
            language = self.get_current_language()
        
        if language not in self.translations:
            language = self.default_language
        
        return self.translations[language]
    
    def get_language_info(self):
        """Get information about current language"""
        current_lang = self.get_current_language()
        
        language_names = {
            'fr': 'Français',
            'en': 'English',
            'es': 'Español',
            'pt': 'Português',
            'de': 'Deutsch',
            'it': 'Italiano',
            'ar': 'العربية'
        }
        
        return {
            'current': current_lang,
            'name': language_names.get(current_lang, current_lang),
            'supported': self.supported_languages,
            'available': {code: language_names.get(code, code) for code in self.supported_languages}
        }
    
    def get_chatbot_language_context(self):
        """Get language context for chatbot responses"""
        current_lang = self.get_current_language()
        
        language_contexts = {
            'fr': {
                'greeting': 'Shalom bien-aimé(e) !',
                'style': 'Réponds en français avec un ton chaleureux et biblique.',
                'blessing': 'Que Dieu te bénisse !',
                'verse_intro': 'Voici des versets bibliques :'
            },
            'en': {
                'greeting': 'Shalom beloved!',
                'style': 'Respond in English with a warm and biblical tone.',
                'blessing': 'May God bless you!',
                'verse_intro': 'Here are biblical verses:'
            },
            'es': {
                'greeting': '¡Shalom querido/a!',
                'style': 'Responde en español con un tono cálido y bíblico.',
                'blessing': '¡Que Dios te bendiga!',
                'verse_intro': 'Aquí están los versículos bíblicos:'
            },
            'pt': {
                'greeting': 'Shalom amado/a!',
                'style': 'Responda em português com um tom caloroso e bíblico.',
                'blessing': 'Que Deus te abençoe!',
                'verse_intro': 'Aqui estão os versículos bíblicos:'
            },
            'de': {
                'greeting': 'Shalom Geliebte/r!',
                'style': 'Antworte auf Deutsch mit einem warmen und biblischen Ton.',
                'blessing': 'Gott segne dich!',
                'verse_intro': 'Hier sind biblische Verse:'
            },
            'it': {
                'greeting': 'Shalom caro/a!',
                'style': 'Rispondi in italiano con un tono caloroso e biblico.',
                'blessing': 'Che Dio ti benedica!',
                'verse_intro': 'Ecco i versetti biblici:'
            },
            'ar': {
                'greeting': 'شالوم حبيبي/حبيبتي!',
                'style': 'اجب باللغة العربية بنبرة دافئة وتوراتية.',
                'blessing': 'بارك الله فيك!',
                'verse_intro': 'هذه آيات من الكتاب المقدس:'
            }
        }
        
        return language_contexts.get(current_lang, language_contexts['fr'])

# Global translation service instance
translation_service = TranslationService()

def get_translation_service():
    """Get the global translation service instance"""
    return translation_service

# Template function for translations
def t(key, language=None):
    """Translation function for templates"""
    return translation_service.translate(key, language)

# Decorator for routes that need language context
def with_language_context(f):
    """Decorator to add language context to routes"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        g.language = translation_service.get_current_language()
        g.translations = translation_service.get_all_translations()
        g.language_info = translation_service.get_language_info()
        g.t = t  # Add translation function to template context
        return f(*args, **kwargs)
    return decorated_function

# Context processor for templates
def register_template_context(app):
    """Register template context processors"""
    @app.context_processor
    def inject_language_context():
        return {
            'current_language': translation_service.get_current_language(),
            'translations': translation_service.get_all_translations(),
            'language_info': translation_service.get_language_info(),
            't': t
        }