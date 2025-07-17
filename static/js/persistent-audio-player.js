// Persistent Audio Player - Continues playing across page navigation
class PersistentAudioPlayer {
    constructor() {
        this.audioElement = null;
        this.currentTrack = null;
        this.currentPlaylist = [];
        this.currentIndex = 0;
        this.isPlaying = false;
        this.volume = 0.8;
        this.repeat = false;
        this.shuffle = false;
        this.miniPlayer = null;
        
        this.init();
    }
    
    init() {
        this.createAudioElement();
        this.createMiniPlayer();
        this.setupEventListeners();
        this.loadSettings();
        this.restoreSession();
    }
    
    createAudioElement() {
        // Create or reuse existing audio element
        this.audioElement = document.getElementById('persistent-audio') || document.createElement('audio');
        this.audioElement.id = 'persistent-audio';
        this.audioElement.preload = 'metadata';
        this.audioElement.style.display = 'none';
        document.body.appendChild(this.audioElement);
        
        // Audio event listeners
        this.audioElement.addEventListener('loadeddata', () => {
            this.updateMiniPlayer();
        });
        
        this.audioElement.addEventListener('timeupdate', () => {
            this.updateProgress();
        });
        
        this.audioElement.addEventListener('ended', () => {
            this.nextTrack();
        });
        
        this.audioElement.addEventListener('error', (e) => {
            console.error('Audio error:', e);
            this.nextTrack();
        });
    }
    
    createMiniPlayer() {
        if (document.getElementById('mini-player')) return;
        
        this.miniPlayer = document.createElement('div');
        this.miniPlayer.id = 'mini-player';
        this.miniPlayer.className = 'fixed bottom-4 right-4 bg-white dark:bg-gray-800 rounded-lg shadow-lg border border-gray-200 dark:border-gray-700 z-50 transition-all duration-300 transform translate-y-full opacity-0';
        this.miniPlayer.style.width = '320px';
        this.miniPlayer.style.minHeight = '80px';
        
        this.miniPlayer.innerHTML = `
            <div class="p-4">
                <div class="flex items-center space-x-3">
                    <div class="bg-orange-100 dark:bg-orange-900 w-12 h-12 rounded-lg flex items-center justify-center flex-shrink-0">
                        <i class="fas fa-music text-orange-600"></i>
                    </div>
                    <div class="flex-1 min-w-0">
                        <h4 id="mini-title" class="font-medium text-gray-900 dark:text-white text-sm truncate">
                            Aucune musique
                        </h4>
                        <p id="mini-description" class="text-xs text-gray-500 dark:text-gray-400 truncate">
                            Sélectionnez une musique
                        </p>
                    </div>
                </div>
                
                <div class="mt-3 space-y-2">
                    <div class="flex items-center space-x-2">
                        <button id="mini-prev" class="text-gray-600 dark:text-gray-400 hover:text-orange-600 dark:hover:text-orange-400 transition-colors">
                            <i class="fas fa-step-backward"></i>
                        </button>
                        <button id="mini-play-pause" class="bg-orange-600 hover:bg-orange-700 text-white w-8 h-8 rounded-full flex items-center justify-center transition-colors">
                            <i class="fas fa-play"></i>
                        </button>
                        <button id="mini-next" class="text-gray-600 dark:text-gray-400 hover:text-orange-600 dark:hover:text-orange-400 transition-colors">
                            <i class="fas fa-step-forward"></i>
                        </button>
                        <div class="flex-1 flex items-center space-x-2">
                            <span id="mini-current-time" class="text-xs text-gray-500 dark:text-gray-400">0:00</span>
                            <input type="range" id="mini-progress" class="flex-1 h-1 bg-gray-200 dark:bg-gray-700 rounded-lg appearance-none cursor-pointer" min="0" max="100" value="0">
                            <span id="mini-duration" class="text-xs text-gray-500 dark:text-gray-400">0:00</span>
                        </div>
                        <button id="mini-close" class="text-gray-400 hover:text-red-500 transition-colors">
                            <i class="fas fa-times"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        
        document.body.appendChild(this.miniPlayer);
    }
    
    setupEventListeners() {
        // Mini player controls
        document.getElementById('mini-play-pause').addEventListener('click', () => {
            this.togglePlayPause();
        });
        
        document.getElementById('mini-prev').addEventListener('click', () => {
            this.prevTrack();
        });
        
        document.getElementById('mini-next').addEventListener('click', () => {
            this.nextTrack();
        });
        
        document.getElementById('mini-progress').addEventListener('input', (e) => {
            this.seek(e.target.value);
        });
        
        document.getElementById('mini-close').addEventListener('click', () => {
            this.hideMiniPlayer();
        });
        
        // Global keyboard shortcuts
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey || e.metaKey) {
                switch(e.key) {
                    case ' ':
                        e.preventDefault();
                        this.togglePlayPause();
                        break;
                    case 'ArrowLeft':
                        e.preventDefault();
                        this.prevTrack();
                        break;
                    case 'ArrowRight':
                        e.preventDefault();
                        this.nextTrack();
                        break;
                }
            }
        });
        
        // Handle page navigation
        window.addEventListener('beforeunload', () => {
            this.saveSession();
        });
    }
    
    // Play a single track
    play(url, title, description = '', adminVolume = 0.7) {
        console.log('Playing track:', { url, title, adminVolume });
        
        this.currentTrack = { url, title, description, adminVolume };
        this.currentPlaylist = [this.currentTrack];
        this.currentIndex = 0;
        
        this.loadAndPlay();
        this.showMiniPlayer();
        this.saveSession();
    }
    
    // Play a playlist
    playPlaylist(playlist, startIndex = 0) {
        console.log('Playing playlist:', playlist);
        
        if (!playlist || playlist.length === 0) return;
        
        this.currentPlaylist = playlist;
        this.currentIndex = startIndex;
        this.currentTrack = playlist[startIndex];
        
        this.loadAndPlay();
        this.showMiniPlayer();
        this.saveSession();
    }
    
    loadAndPlay() {
        if (!this.currentTrack) return;
        
        this.audioElement.src = this.currentTrack.url;
        this.audioElement.load();
        
        // Set volume (admin setting for users)
        const isAdminMode = window.location.pathname.includes('/admin/') || 
                          document.getElementById('add-audio-modal');
        
        if (isAdminMode) {
            this.audioElement.volume = this.currentTrack.adminVolume * this.volume;
        } else {
            this.audioElement.volume = this.currentTrack.adminVolume;
        }
        
        this.audioElement.addEventListener('canplay', () => {
            this.audioElement.play()
                .then(() => {
                    this.isPlaying = true;
                    this.updateMiniPlayer();
                    console.log('Persistent audio started:', this.currentTrack.title);
                })
                .catch(error => {
                    console.error('Error playing persistent audio:', error);
                });
        }, { once: true });
    }
    
    togglePlayPause() {
        if (!this.audioElement || !this.currentTrack) return;
        
        if (this.isPlaying) {
            this.audioElement.pause();
            this.isPlaying = false;
        } else {
            this.audioElement.play()
                .then(() => {
                    this.isPlaying = true;
                })
                .catch(error => {
                    console.error('Error resuming playback:', error);
                });
        }
        
        this.updateMiniPlayer();
    }
    
    nextTrack() {
        if (this.currentPlaylist.length <= 1) return;
        
        if (this.shuffle) {
            this.currentIndex = Math.floor(Math.random() * this.currentPlaylist.length);
        } else {
            this.currentIndex = (this.currentIndex + 1) % this.currentPlaylist.length;
        }
        
        this.currentTrack = this.currentPlaylist[this.currentIndex];
        this.loadAndPlay();
    }
    
    prevTrack() {
        if (this.currentPlaylist.length <= 1) return;
        
        if (this.shuffle) {
            this.currentIndex = Math.floor(Math.random() * this.currentPlaylist.length);
        } else {
            this.currentIndex = this.currentIndex === 0 ? this.currentPlaylist.length - 1 : this.currentIndex - 1;
        }
        
        this.currentTrack = this.currentPlaylist[this.currentIndex];
        this.loadAndPlay();
    }
    
    seek(percentage) {
        if (!this.audioElement || !this.currentTrack) return;
        
        const seekTime = (percentage / 100) * this.audioElement.duration;
        this.audioElement.currentTime = seekTime;
    }
    
    updateProgress() {
        if (!this.audioElement || !this.currentTrack) return;
        
        const currentTime = this.audioElement.currentTime;
        const duration = this.audioElement.duration;
        
        if (duration > 0) {
            const progress = (currentTime / duration) * 100;
            document.getElementById('mini-progress').value = progress;
            
            document.getElementById('mini-current-time').textContent = this.formatTime(currentTime);
            document.getElementById('mini-duration').textContent = this.formatTime(duration);
        }
    }
    
    updateMiniPlayer() {
        if (!this.currentTrack) return;
        
        document.getElementById('mini-title').textContent = this.currentTrack.title;
        document.getElementById('mini-description').textContent = this.currentTrack.description || '';
        
        const playPauseBtn = document.getElementById('mini-play-pause');
        const icon = playPauseBtn.querySelector('i');
        
        if (this.isPlaying) {
            icon.className = 'fas fa-pause';
        } else {
            icon.className = 'fas fa-play';
        }
        
        // Update navigation buttons
        const prevBtn = document.getElementById('mini-prev');
        const nextBtn = document.getElementById('mini-next');
        
        if (this.currentPlaylist.length > 1) {
            prevBtn.style.opacity = '1';
            nextBtn.style.opacity = '1';
            prevBtn.style.pointerEvents = 'auto';
            nextBtn.style.pointerEvents = 'auto';
        } else {
            prevBtn.style.opacity = '0.5';
            nextBtn.style.opacity = '0.5';
            prevBtn.style.pointerEvents = 'none';
            nextBtn.style.pointerEvents = 'none';
        }
    }
    
    showMiniPlayer() {
        if (this.miniPlayer) {
            this.miniPlayer.style.transform = 'translateY(0)';
            this.miniPlayer.style.opacity = '1';
        }
    }
    
    hideMiniPlayer() {
        if (this.miniPlayer) {
            this.miniPlayer.style.transform = 'translateY(100%)';
            this.miniPlayer.style.opacity = '0';
        }
        
        // Stop current playback
        if (this.audioElement) {
            this.audioElement.pause();
            this.isPlaying = false;
        }
        
        this.currentTrack = null;
        this.saveSession();
    }
    
    formatTime(seconds) {
        if (isNaN(seconds)) return '0:00';
        
        const minutes = Math.floor(seconds / 60);
        const remainingSeconds = Math.floor(seconds % 60);
        return `${minutes}:${remainingSeconds.toString().padStart(2, '0')}`;
    }
    
    saveSession() {
        const sessionData = {
            currentTrack: this.currentTrack,
            currentPlaylist: this.currentPlaylist,
            currentIndex: this.currentIndex,
            isPlaying: this.isPlaying,
            currentTime: this.audioElement ? this.audioElement.currentTime : 0,
            volume: this.volume
        };
        
        localStorage.setItem('benj-persistent-audio-session', JSON.stringify(sessionData));
    }
    
    restoreSession() {
        const sessionData = localStorage.getItem('benj-persistent-audio-session');
        if (!sessionData) return;
        
        try {
            const data = JSON.parse(sessionData);
            
            if (data.currentTrack) {
                this.currentTrack = data.currentTrack;
                this.currentPlaylist = data.currentPlaylist || [data.currentTrack];
                this.currentIndex = data.currentIndex || 0;
                this.volume = data.volume || 0.8;
                
                // Load track but don't auto-play
                this.audioElement.src = this.currentTrack.url;
                this.audioElement.load();
                
                if (data.currentTime) {
                    this.audioElement.currentTime = data.currentTime;
                }
                
                this.updateMiniPlayer();
                this.showMiniPlayer();
                
                // Only auto-resume if was playing
                if (data.isPlaying) {
                    this.audioElement.addEventListener('canplay', () => {
                        this.audioElement.play().then(() => {
                            this.isPlaying = true;
                            this.updateMiniPlayer();
                        }).catch(error => {
                            console.log('Auto-resume failed (user interaction required):', error);
                        });
                    }, { once: true });
                }
            }
        } catch (error) {
            console.error('Error restoring audio session:', error);
        }
    }
    
    loadSettings() {
        const settings = localStorage.getItem('benj-persistent-audio-settings');
        if (settings) {
            try {
                const data = JSON.parse(settings);
                this.volume = data.volume || 0.8;
                this.repeat = data.repeat || false;
                this.shuffle = data.shuffle || false;
            } catch (error) {
                console.error('Error loading settings:', error);
            }
        }
    }
    
    saveSettings() {
        const settings = {
            volume: this.volume,
            repeat: this.repeat,
            shuffle: this.shuffle
        };
        
        localStorage.setItem('benj-persistent-audio-settings', JSON.stringify(settings));
    }
    
    // Public methods for external use
    stop() {
        if (this.audioElement) {
            this.audioElement.pause();
            this.audioElement.currentTime = 0;
        }
        this.isPlaying = false;
        this.hideMiniPlayer();
    }
    
    getCurrentTrack() {
        return this.currentTrack;
    }
    
    isCurrentlyPlaying() {
        return this.isPlaying;
    }
    
    getPlaylist() {
        return this.currentPlaylist;
    }
}

// Initialize persistent audio player when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    if (!window.persistentAudioPlayer) {
        window.persistentAudioPlayer = new PersistentAudioPlayer();
        console.log('Persistent Audio Player initialized');
    }
});

// Global functions for easy access
function playPersistentAudio(url, title, description = '', adminVolume = 0.7) {
    if (window.persistentAudioPlayer) {
        window.persistentAudioPlayer.play(url, title, description, adminVolume);
    }
}

function playPersistentPlaylist(playlist, startIndex = 0) {
    if (window.persistentAudioPlayer) {
        window.persistentAudioPlayer.playPlaylist(playlist, startIndex);
    }
}

function stopPersistentAudio() {
    if (window.persistentAudioPlayer) {
        window.persistentAudioPlayer.stop();
    }
}