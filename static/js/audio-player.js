// Audio Player for BENJ INSIDE Playlist
(function() {
    'use strict';
    
    const AudioPlayer = {
        // Player elements
        currentPlayer: null,
        audioElement: null,
        progressBar: null,
        volumeControl: null,
        playPauseBtn: null,
        stopBtn: null,
        currentTimeDisplay: null,
        durationDisplay: null,
        currentTitle: null,
        currentDescription: null,
        
        // Player state
        isPlaying: false,
        currentTrack: null,
        currentPosition: 0,
        volume: 0.5,
        
        // Initialize audio player
        init: function() {
            this.setupElements();
            this.setupEventListeners();
            this.loadSettings();
            console.log('Audio Player initialized');
        },
        
        // Setup DOM elements
        setupElements: function() {
            this.currentPlayer = document.getElementById('current-player');
            this.audioElement = document.getElementById('audio-player');
            this.progressBar = document.getElementById('progress-bar');
            this.volumeControl = document.getElementById('volume-control');
            this.playPauseBtn = document.getElementById('play-pause-btn');
            this.stopBtn = document.getElementById('stop-btn');
            this.currentTimeDisplay = document.getElementById('current-time');
            this.durationDisplay = document.getElementById('duration');
            this.currentTitle = document.getElementById('current-title');
            this.currentDescription = document.getElementById('current-description');
        },
        
        // Setup event listeners
        setupEventListeners: function() {
            if (!this.audioElement) return;
            
            // Audio element events
            this.audioElement.addEventListener('loadedmetadata', () => {
                this.updateDuration();
                this.updateProgressBar();
            });
            
            this.audioElement.addEventListener('timeupdate', () => {
                this.updateTime();
                this.updateProgressBar();
            });
            
            this.audioElement.addEventListener('ended', () => {
                this.onTrackEnded();
            });
            
            this.audioElement.addEventListener('error', (e) => {
                this.onError(e);
            });
            
            this.audioElement.addEventListener('loadstart', () => {
                this.showLoading();
            });
            
            this.audioElement.addEventListener('canplay', () => {
                this.hideLoading();
            });
            
            // Control buttons
            if (this.playPauseBtn) {
                this.playPauseBtn.addEventListener('click', () => {
                    this.togglePlayPause();
                });
            }
            
            if (this.stopBtn) {
                this.stopBtn.addEventListener('click', () => {
                    this.stop();
                });
            }
            
            // Progress bar
            if (this.progressBar) {
                this.progressBar.addEventListener('input', () => {
                    this.seek();
                });
            }
            
            // Volume control
            if (this.volumeControl) {
                this.volumeControl.addEventListener('input', () => {
                    this.updateVolume();
                });
            }
            
            // Keyboard shortcuts
            document.addEventListener('keydown', (e) => {
                if (this.currentTrack) {
                    this.handleKeyboard(e);
                }
            });
        },
        
        // Load audio and start playing
        play: function(url, title, description = '', adminVolume = 0.7) {
            if (!this.audioElement) return;
            
            console.log('Playing audio:', { url, title, adminVolume });
            
            this.currentTrack = { url, title, description, adminVolume };
            
            // Update UI
            this.updateTrackInfo(title, description);
            this.showPlayer();
            
            // Load and play audio
            this.audioElement.src = url;
            this.audioElement.load();
            
            // Set volume immediately
            const userVolumeMultiplier = this.volume; // User's volume preference (0.0 - 1.0)
            const finalVolume = Math.min(1.0, adminVolume * userVolumeMultiplier);
            this.audioElement.volume = finalVolume;
            
            console.log('Volume set to:', finalVolume, 'Admin:', adminVolume, 'User:', userVolumeMultiplier);
            
            // Play when ready
            this.audioElement.addEventListener('canplay', () => {
                console.log('Audio can play, attempting to start playback');
                
                this.audioElement.play()
                    .then(() => {
                        console.log('Audio playback started successfully');
                        this.isPlaying = true;
                        this.updatePlayPauseButton();
                        this.saveCurrentTrack();
                    })
                    .catch(error => {
                        console.error('Error playing audio:', error);
                        this.showError('Erreur lors de la lecture audio: ' + error.message);
                    });
            }, { once: true });
            
            // Add error handling
            this.audioElement.addEventListener('error', (e) => {
                console.error('Audio error:', e);
                this.showError('Erreur de chargement audio');
            }, { once: true });
        },
        
        // Toggle play/pause
        togglePlayPause: function() {
            if (!this.audioElement || !this.currentTrack) return;
            
            if (this.isPlaying) {
                this.pause();
            } else {
                this.resume();
            }
        },
        
        // Pause playback
        pause: function() {
            if (this.audioElement && this.isPlaying) {
                this.audioElement.pause();
                this.isPlaying = false;
                this.updatePlayPauseButton();
            }
        },
        
        // Resume playback
        resume: function() {
            if (this.audioElement && !this.isPlaying) {
                this.audioElement.play()
                    .then(() => {
                        this.isPlaying = true;
                        this.updatePlayPauseButton();
                    })
                    .catch(error => {
                        console.error('Error resuming audio:', error);
                        this.showError('Erreur lors de la reprise');
                    });
            }
        },
        
        // Stop playback
        stop: function() {
            if (this.audioElement) {
                this.audioElement.pause();
                this.audioElement.currentTime = 0;
                this.isPlaying = false;
                this.updatePlayPauseButton();
                this.updateTime();
                this.updateProgressBar();
                this.hidePlayer();
                this.currentTrack = null;
                this.clearCurrentTrack();
            }
        },
        
        // Seek to position
        seek: function() {
            if (this.audioElement && this.progressBar) {
                const seekTime = (this.progressBar.value / 100) * this.audioElement.duration;
                this.audioElement.currentTime = seekTime;
            }
        },
        
        // Update volume
        updateVolume: function() {
            if (this.audioElement && this.volumeControl) {
                this.volume = this.volumeControl.value / 100;
                
                // Apply admin volume setting if available
                if (this.currentTrack && this.currentTrack.adminVolume) {
                    const finalVolume = this.currentTrack.adminVolume * this.volume;
                    this.audioElement.volume = finalVolume;
                } else {
                    this.audioElement.volume = this.volume;
                }
                
                this.saveSettings();
            }
        },
        
        // Update track info display
        updateTrackInfo: function(title, description) {
            if (this.currentTitle) {
                this.currentTitle.textContent = title;
            }
            if (this.currentDescription) {
                this.currentDescription.textContent = description;
            }
        },
        
        // Update play/pause button
        updatePlayPauseButton: function() {
            if (this.playPauseBtn) {
                const icon = this.playPauseBtn.querySelector('i');
                if (icon) {
                    if (this.isPlaying) {
                        icon.className = 'fas fa-pause';
                    } else {
                        icon.className = 'fas fa-play';
                    }
                }
            }
        },
        
        // Update time display
        updateTime: function() {
            if (this.audioElement) {
                const currentTime = this.audioElement.currentTime;
                if (this.currentTimeDisplay) {
                    this.currentTimeDisplay.textContent = this.formatTime(currentTime);
                }
            }
        },
        
        // Update duration display
        updateDuration: function() {
            if (this.audioElement && this.durationDisplay) {
                const duration = this.audioElement.duration;
                if (!isNaN(duration)) {
                    this.durationDisplay.textContent = this.formatTime(duration);
                }
            }
        },
        
        // Update progress bar
        updateProgressBar: function() {
            if (this.audioElement && this.progressBar) {
                const duration = this.audioElement.duration;
                const currentTime = this.audioElement.currentTime;
                
                if (duration > 0) {
                    const progress = (currentTime / duration) * 100;
                    this.progressBar.value = progress;
                }
            }
        },
        
        // Format time in MM:SS format
        formatTime: function(seconds) {
            if (isNaN(seconds)) return '0:00';
            
            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = Math.floor(seconds % 60);
            
            return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
        },
        
        // Show player
        showPlayer: function() {
            if (this.currentPlayer) {
                this.currentPlayer.classList.remove('hidden');
            }
        },
        
        // Hide player
        hidePlayer: function() {
            if (this.currentPlayer) {
                this.currentPlayer.classList.add('hidden');
            }
        },
        
        // Show loading state
        showLoading: function() {
            if (this.playPauseBtn) {
                const icon = this.playPauseBtn.querySelector('i');
                if (icon) {
                    icon.className = 'fas fa-spinner fa-spin';
                }
            }
        },
        
        // Hide loading state
        hideLoading: function() {
            if (this.playPauseBtn) {
                this.updatePlayPauseButton();
            }
        },
        
        // Handle track ended
        onTrackEnded: function() {
            this.isPlaying = false;
            this.updatePlayPauseButton();
            this.audioElement.currentTime = 0;
            this.updateTime();
            this.updateProgressBar();
            
            // Auto-hide player after track ends
            setTimeout(() => {
                this.hidePlayer();
            }, 3000);
        },
        
        // Handle errors
        onError: function(error) {
            console.error('Audio error:', error);
            this.showError('Erreur lors du chargement de l\'audio');
            this.hideLoading();
        },
        
        // Show error message
        showError: function(message) {
            if (window.showNotification) {
                window.showNotification(message, 'error');
            } else {
                alert(message);
            }
        },
        
        // Handle keyboard shortcuts
        handleKeyboard: function(event) {
            // Don't handle if user is typing in an input
            if (event.target.tagName === 'INPUT' || event.target.tagName === 'TEXTAREA') {
                return;
            }
            
            switch (event.key) {
                case ' ':
                    event.preventDefault();
                    this.togglePlayPause();
                    break;
                case 'ArrowLeft':
                    event.preventDefault();
                    this.skipBackward();
                    break;
                case 'ArrowRight':
                    event.preventDefault();
                    this.skipForward();
                    break;
                case 'ArrowUp':
                    event.preventDefault();
                    this.increaseVolume();
                    break;
                case 'ArrowDown':
                    event.preventDefault();
                    this.decreaseVolume();
                    break;
            }
        },
        
        // Skip backward (10 seconds)
        skipBackward: function() {
            if (this.audioElement) {
                this.audioElement.currentTime = Math.max(0, this.audioElement.currentTime - 10);
            }
        },
        
        // Skip forward (10 seconds)
        skipForward: function() {
            if (this.audioElement) {
                this.audioElement.currentTime = Math.min(
                    this.audioElement.duration,
                    this.audioElement.currentTime + 10
                );
            }
        },
        
        // Increase volume
        increaseVolume: function() {
            if (this.volumeControl) {
                const newVolume = Math.min(100, parseInt(this.volumeControl.value) + 10);
                this.volumeControl.value = newVolume;
                this.updateVolume();
            }
        },
        
        // Decrease volume
        decreaseVolume: function() {
            if (this.volumeControl) {
                const newVolume = Math.max(0, parseInt(this.volumeControl.value) - 10);
                this.volumeControl.value = newVolume;
                this.updateVolume();
            }
        },
        
        // Save settings to localStorage
        saveSettings: function() {
            const settings = {
                volume: this.volume
            };
            localStorage.setItem('benj-inside-audio-settings', JSON.stringify(settings));
        },
        
        // Load settings from localStorage
        loadSettings: function() {
            const savedSettings = localStorage.getItem('benj-inside-audio-settings');
            if (savedSettings) {
                try {
                    const settings = JSON.parse(savedSettings);
                    if (settings.volume !== undefined) {
                        this.volume = settings.volume;
                        if (this.volumeControl) {
                            this.volumeControl.value = this.volume * 100;
                        }
                        if (this.audioElement) {
                            this.audioElement.volume = this.volume;
                        }
                    }
                } catch (e) {
                    console.error('Error loading audio settings:', e);
                }
            } else {
                // Set default volume to 0.8 (80%) for better audibility
                this.volume = 0.8;
                if (this.volumeControl) {
                    this.volumeControl.value = 80;
                }
                if (this.audioElement) {
                    this.audioElement.volume = this.volume;
                }
            }
        },
        
        // Save current track
        saveCurrentTrack: function() {
            if (this.currentTrack) {
                localStorage.setItem('benj-inside-current-track', JSON.stringify(this.currentTrack));
            }
        },
        
        // Clear current track
        clearCurrentTrack: function() {
            localStorage.removeItem('benj-inside-current-track');
        }
    };
    
    // Global function to play audio (called from template)
    window.playAudio = function(url, title, description, adminVolume) {
        AudioPlayer.play(url, title, description, adminVolume);
    };
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        AudioPlayer.init();
    });
    
    // Export to global scope
    window.AudioPlayer = AudioPlayer;
    
})();
