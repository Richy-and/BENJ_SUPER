/**
 * Language Switcher Component for BENJ INSIDE
 * Handles dynamic language switching without page reload
 */

class LanguageSwitcher {
    constructor() {
        this.currentLanguage = this.getCurrentLanguage();
        this.translations = {};
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadTranslations();
    }

    getCurrentLanguage() {
        // Get from localStorage or default to 'fr'
        return localStorage.getItem('userLanguage') || 'fr';
    }

    bindEvents() {
        // Bind language selector events
        document.addEventListener('DOMContentLoaded', () => {
            const languageSelectors = document.querySelectorAll('.language-selector');
            
            languageSelectors.forEach(selector => {
                selector.addEventListener('change', (e) => {
                    this.changeLanguage(e.target.value);
                });
            });

            // Bind language buttons if they exist
            const languageButtons = document.querySelectorAll('.language-btn');
            languageButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    e.preventDefault();
                    const language = e.target.dataset.language;
                    this.changeLanguage(language);
                });
            });
        });
    }

    async changeLanguage(languageCode) {
        try {
            // Show loading state
            this.showLoadingState();

            // Make API call to change language
            const response = await fetch(`/set-language/${languageCode}`, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                }
            });

            if (response.ok) {
                const result = await response.json();
                
                // Update localStorage
                localStorage.setItem('userLanguage', languageCode);
                this.currentLanguage = languageCode;

                // Update UI elements
                await this.updateUILanguage(languageCode);
                
                // Show success message
                this.showNotification(result.message || 'Language changed successfully', 'success');
                
                // Reload page to apply all changes
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } else {
                throw new Error('Failed to change language');
            }
        } catch (error) {
            console.error('Error changing language:', error);
            this.showNotification('Error changing language. Please try again.', 'error');
        } finally {
            this.hideLoadingState();
        }
    }

    async loadTranslations() {
        try {
            // Load translations from the server
            const response = await fetch('/api/translations');
            if (response.ok) {
                this.translations = await response.json();
            }
        } catch (error) {
            console.error('Error loading translations:', error);
        }
    }

    async updateUILanguage(languageCode) {
        // Update all text elements with data-translate attributes
        const translateElements = document.querySelectorAll('[data-translate]');
        
        translateElements.forEach(element => {
            const key = element.getAttribute('data-translate');
            const translation = this.getTranslation(key, languageCode);
            
            if (translation) {
                if (element.tagName === 'INPUT' && element.type === 'text') {
                    element.placeholder = translation;
                } else {
                    element.textContent = translation;
                }
            }
        });

        // Update language selector values
        const languageSelectors = document.querySelectorAll('.language-selector');
        languageSelectors.forEach(selector => {
            selector.value = languageCode;
        });

        // Update document language attribute
        document.documentElement.lang = languageCode;
    }

    getTranslation(key, languageCode) {
        if (this.translations[languageCode] && this.translations[languageCode][key]) {
            return this.translations[languageCode][key];
        }
        return null;
    }

    showLoadingState() {
        const loadingElements = document.querySelectorAll('.language-loading');
        loadingElements.forEach(element => {
            element.style.display = 'block';
        });
    }

    hideLoadingState() {
        const loadingElements = document.querySelectorAll('.language-loading');
        loadingElements.forEach(element => {
            element.style.display = 'none';
        });
    }

    showNotification(message, type = 'info') {
        // Create notification element
        const notification = document.createElement('div');
        notification.className = `notification notification-${type} fixed top-4 right-4 z-50 p-4 rounded-lg shadow-lg transition-all duration-300`;
        
        // Style based on type
        if (type === 'success') {
            notification.classList.add('bg-green-500', 'text-white');
        } else if (type === 'error') {
            notification.classList.add('bg-red-500', 'text-white');
        } else {
            notification.classList.add('bg-blue-500', 'text-white');
        }
        
        notification.textContent = message;
        
        // Add to document
        document.body.appendChild(notification);
        
        // Remove after 3 seconds
        setTimeout(() => {
            notification.remove();
        }, 3000);
    }

    // Method to update chatbot language dynamically
    updateChatbotLanguage(languageCode) {
        // Update any chatbot-specific language settings
        const chatbotElements = document.querySelectorAll('.chatbot-interface');
        chatbotElements.forEach(element => {
            element.setAttribute('data-language', languageCode);
        });
    }
}

// Initialize language switcher when DOM is ready
document.addEventListener('DOMContentLoaded', () => {
    window.languageSwitcher = new LanguageSwitcher();
});

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = LanguageSwitcher;
}