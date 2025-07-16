// Theme Toggle Functionality for BENJ INSIDE
(function() {
    'use strict';
    
    // Theme management
    const ThemeManager = {
        // Theme storage key
        STORAGE_KEY: 'benj-inside-theme',
        
        // Available themes
        THEMES: {
            LIGHT: 'light',
            DARK: 'dark',
            SYSTEM: 'system'
        },
        
        // Current theme
        currentTheme: 'system',
        
        // Initialize theme manager
        init: function() {
            this.loadTheme();
            this.setupEventListeners();
            this.setupSystemThemeListener();
            this.applyTheme();
        },
        
        // Load theme from localStorage
        loadTheme: function() {
            const savedTheme = localStorage.getItem(this.STORAGE_KEY);
            if (savedTheme && Object.values(this.THEMES).includes(savedTheme)) {
                this.currentTheme = savedTheme;
            }
        },
        
        // Save theme to localStorage
        saveTheme: function() {
            localStorage.setItem(this.STORAGE_KEY, this.currentTheme);
        },
        
        // Setup event listeners
        setupEventListeners: function() {
            const themeToggle = document.getElementById('theme-toggle');
            if (themeToggle) {
                themeToggle.addEventListener('click', () => {
                    this.toggleTheme();
                });
            }
            
            // Theme selector dropdown (if exists)
            const themeSelector = document.getElementById('theme-selector');
            if (themeSelector) {
                themeSelector.addEventListener('change', (e) => {
                    this.setTheme(e.target.value);
                });
            }
        },
        
        // Setup system theme change listener
        setupSystemThemeListener: function() {
            if (window.matchMedia) {
                const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
                mediaQuery.addEventListener('change', () => {
                    if (this.currentTheme === this.THEMES.SYSTEM) {
                        this.applyTheme();
                    }
                });
            }
        },
        
        // Toggle between light and dark theme
        toggleTheme: function() {
            if (this.currentTheme === this.THEMES.LIGHT) {
                this.setTheme(this.THEMES.DARK);
            } else {
                this.setTheme(this.THEMES.LIGHT);
            }
        },
        
        // Set specific theme
        setTheme: function(theme) {
            if (Object.values(this.THEMES).includes(theme)) {
                this.currentTheme = theme;
                this.saveTheme();
                this.applyTheme();
                this.updateThemeIcon();
                this.notifyThemeChange();
            }
        },
        
        // Apply theme to document
        applyTheme: function() {
            const html = document.documentElement;
            
            // Remove existing theme classes
            html.classList.remove('light', 'dark');
            
            // Determine effective theme
            let effectiveTheme = this.currentTheme;
            if (this.currentTheme === this.THEMES.SYSTEM) {
                effectiveTheme = this.getSystemTheme();
            }
            
            // Apply theme class
            if (effectiveTheme === this.THEMES.DARK) {
                html.classList.add('dark');
            } else {
                html.classList.add('light');
            }
            
            // Update theme color meta tag
            this.updateThemeColor(effectiveTheme);
        },
        
        // Get system theme preference
        getSystemTheme: function() {
            if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
                return this.THEMES.DARK;
            }
            return this.THEMES.LIGHT;
        },
        
        // Update theme toggle icon
        updateThemeIcon: function() {
            const themeToggle = document.getElementById('theme-toggle');
            if (!themeToggle) return;
            
            const lightIcon = themeToggle.querySelector('.fa-moon');
            const darkIcon = themeToggle.querySelector('.fa-sun');
            
            if (lightIcon && darkIcon) {
                const isDark = document.documentElement.classList.contains('dark');
                
                if (isDark) {
                    lightIcon.style.display = 'none';
                    darkIcon.style.display = 'inline-block';
                } else {
                    lightIcon.style.display = 'inline-block';
                    darkIcon.style.display = 'none';
                }
            }
        },
        
        // Update theme color meta tag
        updateThemeColor: function(theme) {
            let themeColorMeta = document.querySelector('meta[name="theme-color"]');
            if (!themeColorMeta) {
                themeColorMeta = document.createElement('meta');
                themeColorMeta.name = 'theme-color';
                document.head.appendChild(themeColorMeta);
            }
            
            // Set theme color based on theme
            const colors = {
                light: '#ffffff',
                dark: '#1f2937'
            };
            
            themeColorMeta.content = colors[theme] || colors.light;
        },
        
        // Notify theme change to other components
        notifyThemeChange: function() {
            const event = new CustomEvent('themechange', {
                detail: {
                    theme: this.currentTheme,
                    effectiveTheme: this.getEffectiveTheme()
                }
            });
            document.dispatchEvent(event);
        },
        
        // Get effective theme (resolved system theme)
        getEffectiveTheme: function() {
            if (this.currentTheme === this.THEMES.SYSTEM) {
                return this.getSystemTheme();
            }
            return this.currentTheme;
        },
        
        // Get current theme
        getCurrentTheme: function() {
            return this.currentTheme;
        }
    };
    
    // Color scheme utilities
    const ColorSchemeManager = {
        // Available color schemes
        SCHEMES: {
            BLUE: 'blue',
            GREEN: 'green',
            PURPLE: 'purple',
            ORANGE: 'orange',
            RED: 'red'
        },
        
        // Current color scheme
        currentScheme: 'blue',
        
        // Storage key
        STORAGE_KEY: 'benj-inside-color-scheme',
        
        // Initialize
        init: function() {
            this.loadColorScheme();
            this.setupEventListeners();
            this.applyColorScheme();
        },
        
        // Load color scheme from localStorage
        loadColorScheme: function() {
            const savedScheme = localStorage.getItem(this.STORAGE_KEY);
            if (savedScheme && Object.values(this.SCHEMES).includes(savedScheme)) {
                this.currentScheme = savedScheme;
            }
        },
        
        // Save color scheme to localStorage
        saveColorScheme: function() {
            localStorage.setItem(this.STORAGE_KEY, this.currentScheme);
        },
        
        // Setup event listeners
        setupEventListeners: function() {
            const colorSchemeSelector = document.getElementById('color-scheme-selector');
            if (colorSchemeSelector) {
                colorSchemeSelector.addEventListener('change', (e) => {
                    this.setColorScheme(e.target.value);
                });
            }
            
            // Color scheme buttons
            const colorButtons = document.querySelectorAll('[data-color-scheme]');
            colorButtons.forEach(button => {
                button.addEventListener('click', (e) => {
                    const scheme = e.target.dataset.colorScheme;
                    this.setColorScheme(scheme);
                });
            });
        },
        
        // Set color scheme
        setColorScheme: function(scheme) {
            if (Object.values(this.SCHEMES).includes(scheme)) {
                this.currentScheme = scheme;
                this.saveColorScheme();
                this.applyColorScheme();
                this.notifyColorSchemeChange();
            }
        },
        
        // Apply color scheme
        applyColorScheme: function() {
            const html = document.documentElement;
            
            // Remove existing color scheme classes
            Object.values(this.SCHEMES).forEach(scheme => {
                html.classList.remove(`scheme-${scheme}`);
            });
            
            // Apply current color scheme
            html.classList.add(`scheme-${this.currentScheme}`);
            
            // Update CSS custom properties
            this.updateCustomProperties();
        },
        
        // Update CSS custom properties
        updateCustomProperties: function() {
            const colors = {
                blue: {
                    50: '#f0f9ff',
                    500: '#3b82f6',
                    600: '#2563eb',
                    700: '#1d4ed8',
                    900: '#1e3a8a'
                },
                green: {
                    50: '#f0fdf4',
                    500: '#22c55e',
                    600: '#16a34a',
                    700: '#15803d',
                    900: '#14532d'
                },
                purple: {
                    50: '#faf5ff',
                    500: '#a855f7',
                    600: '#9333ea',
                    700: '#7c3aed',
                    900: '#581c87'
                },
                orange: {
                    50: '#fff7ed',
                    500: '#f97316',
                    600: '#ea580c',
                    700: '#c2410c',
                    900: '#9a3412'
                },
                red: {
                    50: '#fef2f2',
                    500: '#ef4444',
                    600: '#dc2626',
                    700: '#b91c1c',
                    900: '#7f1d1d'
                }
            };
            
            const schemeColors = colors[this.currentScheme];
            if (schemeColors) {
                const root = document.documentElement;
                Object.entries(schemeColors).forEach(([shade, color]) => {
                    root.style.setProperty(`--color-primary-${shade}`, color);
                });
            }
        },
        
        // Notify color scheme change
        notifyColorSchemeChange: function() {
            const event = new CustomEvent('colorschemechange', {
                detail: { scheme: this.currentScheme }
            });
            document.dispatchEvent(event);
        },
        
        // Get current color scheme
        getCurrentColorScheme: function() {
            return this.currentScheme;
        }
    };
    
    // Theme persistence across page loads
    const ThemePersistence = {
        // Apply theme immediately (before page render)
        applyImmediate: function() {
            const savedTheme = localStorage.getItem('benj-inside-theme') || 'system';
            let effectiveTheme = savedTheme;
            
            if (savedTheme === 'system') {
                effectiveTheme = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
            }
            
            if (effectiveTheme === 'dark') {
                document.documentElement.classList.add('dark');
            } else {
                document.documentElement.classList.add('light');
            }
        }
    };
    
    // Initialize theme immediately
    ThemePersistence.applyImmediate();
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        ThemeManager.init();
        ColorSchemeManager.init();
        
        // Listen for theme changes
        document.addEventListener('themechange', function(e) {
            console.log('Theme changed to:', e.detail.theme);
        });
        
        document.addEventListener('colorschemechange', function(e) {
            console.log('Color scheme changed to:', e.detail.scheme);
        });
    });
    
    // Export to global scope
    window.ThemeManager = ThemeManager;
    window.ColorSchemeManager = ColorSchemeManager;
    
})();
