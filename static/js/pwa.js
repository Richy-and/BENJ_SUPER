// PWA Installation et gestion
class PWAManager {
    constructor() {
        this.deferredPrompt = null;
        this.isInstalled = false;
        this.init();
    }

    init() {
        // Enregistrer le Service Worker
        this.registerServiceWorker();
        
        // Gérer l'événement d'installation
        this.handleInstallPrompt();
        
        // Créer le bouton d'installation
        this.createInstallButton();
        
        // Vérifier si l'app est déjà installée
        this.checkIfInstalled();
        
        // Gérer les mises à jour
        this.handleUpdates();
    }

    async registerServiceWorker() {
        if ('serviceWorker' in navigator) {
            try {
                const registration = await navigator.serviceWorker.register('/sw.js');
                console.log('Service Worker enregistré:', registration);
                
                // Écouter les mises à jour
                registration.addEventListener('updatefound', () => {
                    const newWorker = registration.installing;
                    newWorker.addEventListener('statechange', () => {
                        if (newWorker.state === 'installed' && navigator.serviceWorker.controller) {
                            this.showUpdateAvailable();
                        }
                    });
                });
                
            } catch (error) {
                console.error('Erreur Service Worker:', error);
            }
        }
    }

    handleInstallPrompt() {
        window.addEventListener('beforeinstallprompt', (e) => {
            // Empêcher l'affichage automatique
            e.preventDefault();
            
            // Sauvegarder l'événement
            this.deferredPrompt = e;
            
            // Montrer le bouton d'installation
            this.showInstallButton();
        });

        // Détecter si l'app a été installée
        window.addEventListener('appinstalled', () => {
            console.log('BENJ INSIDE installée avec succès!');
            this.hideInstallButton();
            this.isInstalled = true;
            this.showInstallSuccessMessage();
        });
    }

    createInstallButton() {
        // Créer le bouton d'installation
        const installButton = document.createElement('button');
        installButton.id = 'pwa-install-btn';
        installButton.innerHTML = `
            <i class="fas fa-download mr-2"></i>
            <span class="hidden sm:inline">Installer l'application</span>
            <span class="sm:hidden">Installer</span>
        `;
        installButton.className = `
            fixed bottom-4 right-4 z-50 bg-blue-600 hover:bg-blue-700 
            text-white px-3 py-2 sm:px-4 sm:py-3 rounded-lg shadow-lg 
            transition-all duration-300 flex items-center font-medium hidden
            backdrop-filter backdrop-blur-sm bg-opacity-90
        `;
        
        installButton.addEventListener('click', () => this.installApp());
        document.body.appendChild(installButton);
        
        // Ajouter aussi un indicateur dans la navigation si possible
        this.addNavInstallIndicator();
    }
    
    addNavInstallIndicator() {
        // Ajouter un petit indicateur dans la navigation pour l'installation PWA
        const nav = document.querySelector('nav .flex.items-center.space-x-4');
        if (nav && !document.getElementById('nav-install-indicator')) {
            const indicator = document.createElement('a');
            indicator.id = 'nav-install-indicator';
            indicator.href = '/install';
            indicator.className = `
                hidden lg:flex items-center space-x-2 text-blue-600 hover:text-blue-700 
                dark:text-blue-400 dark:hover:text-blue-300 transition-colors
                px-3 py-2 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/20
            `;
            indicator.innerHTML = `
                <i class="fas fa-mobile-alt text-sm"></i>
                <span class="text-sm font-medium">Installer l'app</span>
            `;
            
            // Insérer avant le bouton WhatsApp
            const whatsappBtn = nav.querySelector('a[href*="wa.me"]');
            if (whatsappBtn) {
                nav.insertBefore(indicator, whatsappBtn);
            } else {
                nav.appendChild(indicator);
            }
        }
    }

    showInstallButton() {
        const button = document.getElementById('pwa-install-btn');
        if (button && !this.isInstalled) {
            button.classList.remove('hidden');
            
            // Animation d'entrée
            setTimeout(() => {
                button.style.transform = 'translateY(0)';
                button.style.opacity = '1';
            }, 100);
        }
    }

    hideInstallButton() {
        const button = document.getElementById('pwa-install-btn');
        if (button) {
            button.style.transform = 'translateY(100px)';
            button.style.opacity = '0';
            setTimeout(() => {
                button.classList.add('hidden');
            }, 300);
        }
    }

    async installApp() {
        if (!this.deferredPrompt) return;

        // Afficher le prompt d'installation
        this.deferredPrompt.prompt();

        // Attendre la réponse utilisateur
        const result = await this.deferredPrompt.userChoice;
        
        if (result.outcome === 'accepted') {
            console.log('Utilisateur a accepté l\'installation');
        } else {
            console.log('Utilisateur a refusé l\'installation');
        }

        // Reset l'événement
        this.deferredPrompt = null;
        this.hideInstallButton();
    }

    checkIfInstalled() {
        // Vérifier si l'app est en mode standalone (installée)
        if (window.matchMedia('(display-mode: standalone)').matches) {
            this.isInstalled = true;
            this.hideInstallButton();
            this.addStandaloneStyles();
        }

        // Vérifier iOS Safari
        if (window.navigator.standalone === true) {
            this.isInstalled = true;
            this.hideInstallButton();
            this.addStandaloneStyles();
        }
    }

    addStandaloneStyles() {
        // Ajouter des styles spécifiques pour le mode app
        document.body.classList.add('pwa-standalone');
        
        // Ajuster le padding pour éviter les notches sur mobile
        const style = document.createElement('style');
        style.textContent = `
            .pwa-standalone {
                padding-top: env(safe-area-inset-top);
                padding-bottom: env(safe-area-inset-bottom);
            }
            
            .pwa-standalone .navbar {
                padding-top: calc(1rem + env(safe-area-inset-top));
            }
        `;
        document.head.appendChild(style);
    }

    showInstallSuccessMessage() {
        // Créer une notification de succès
        const notification = document.createElement('div');
        notification.className = `
            fixed top-4 right-4 z-50 bg-green-600 text-white px-6 py-4 
            rounded-lg shadow-lg flex items-center space-x-3 max-w-sm
        `;
        notification.innerHTML = `
            <i class="fas fa-check-circle text-xl"></i>
            <div>
                <div class="font-medium">Application installée!</div>
                <div class="text-sm opacity-90">BENJ INSIDE est maintenant accessible depuis votre écran d'accueil</div>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Supprimer après 5 secondes
        setTimeout(() => {
            notification.remove();
        }, 5000);
    }

    showUpdateAvailable() {
        // Notification de mise à jour disponible
        const updateNotification = document.createElement('div');
        updateNotification.className = `
            fixed top-4 left-4 right-4 z-50 bg-blue-600 text-white px-6 py-4 
            rounded-lg shadow-lg flex items-center justify-between
        `;
        updateNotification.innerHTML = `
            <div class="flex items-center space-x-3">
                <i class="fas fa-sync-alt text-xl"></i>
                <div>
                    <div class="font-medium">Mise à jour disponible</div>
                    <div class="text-sm opacity-90">Une nouvelle version est prête</div>
                </div>
            </div>
            <button onclick="window.location.reload()" class="bg-white text-blue-600 px-4 py-2 rounded font-medium hover:bg-gray-100">
                Actualiser
            </button>
        `;
        
        document.body.appendChild(updateNotification);
        
        // Supprimer après 10 secondes si pas d'action
        setTimeout(() => {
            if (updateNotification.parentNode) {
                updateNotification.remove();
            }
        }, 10000);
    }

    handleUpdates() {
        // Vérifier les mises à jour périodiquement
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.addEventListener('controllerchange', () => {
                window.location.reload();
            });
        }
    }
}

// Initialiser le PWA Manager quand le DOM est prêt
document.addEventListener('DOMContentLoaded', () => {
    window.pwaManager = new PWAManager();
});

// Gérer les erreurs réseau
window.addEventListener('online', () => {
    console.log('Connexion rétablie');
    // Optionnel: afficher une notification
});

window.addEventListener('offline', () => {
    console.log('Mode hors ligne');
    // Optionnel: afficher une notification
});