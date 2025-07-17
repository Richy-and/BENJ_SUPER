// Chatbot Interface for BENJ INSIDE - Kadosh.ia
(function() {
    'use strict';
    
    const Chatbot = {
        // DOM elements
        chatMessages: null,
        chatInput: null,
        sendBtn: null,
        
        // State
        isLoading: false,
        messageHistory: [],
        
        // Initialize chatbot
        init: function() {
            this.setupElements();
            this.setupEventListeners();
            this.loadMessageHistory();
            console.log('Kadosh.ia Chatbot initialized');
        },
        
        // Setup DOM elements
        setupElements: function() {
            this.chatMessages = document.getElementById('chat-messages');
            this.chatInput = document.getElementById('chat-input');
            this.sendBtn = document.getElementById('send-btn');
        },
        
        // Setup event listeners
        setupEventListeners: function() {
            if (this.sendBtn) {
                this.sendBtn.addEventListener('click', () => {
                    this.sendMessage();
                });
            }
            
            if (this.chatInput) {
                this.chatInput.addEventListener('keypress', (e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                        e.preventDefault();
                        this.sendMessage();
                    }
                });
                
                // Auto-resize textarea
                this.chatInput.addEventListener('input', () => {
                    this.autoResizeInput();
                });
            }
        },
        
        // Send message
        sendMessage: function() {
            if (this.isLoading) return;
            
            const message = this.chatInput.value.trim();
            if (!message) return;
            
            // Add user message to chat
            this.addMessage(message, 'user');
            
            // Clear input
            this.chatInput.value = '';
            this.autoResizeInput();
            
            // Show loading
            this.showLoading();
            
            // Send to server
            this.sendToServer(message);
        },
        
        // Send message to server
        sendToServer: function(message) {
            fetch('/chatbot/ask', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ question: message })
            })
            .then(response => response.json())
            .then(data => {
                this.hideLoading();
                
                if (data.error) {
                    this.addMessage(`Erreur: ${data.error}`, 'bot', 'error');
                } else {
                    this.addMessage(data.response, 'bot', data.source);
                }
            })
            .catch(error => {
                console.error('Error sending message:', error);
                this.hideLoading();
                this.addMessage('Désolé, une erreur est survenue. Veuillez réessayer.', 'bot', 'error');
            });
        },
        
        // Add message to chat
        addMessage: function(content, sender, source = null) {
            if (!this.chatMessages) return;
            
            const messageDiv = document.createElement('div');
            messageDiv.className = 'flex items-start space-x-3 fade-in';
            
            if (sender === 'user') {
                messageDiv.classList.add('justify-end');
                messageDiv.innerHTML = `
                    <div class="bg-primary-600 text-white rounded-lg p-3 max-w-md">
                        <p class="text-sm">${this.escapeHtml(content)}</p>
                    </div>
                    <div class="bg-primary-600 w-8 h-8 rounded-full flex items-center justify-center">
                        <i class="fas fa-user text-white text-sm"></i>
                    </div>
                `;
            } else {
                messageDiv.innerHTML = `
                    <div class="w-8 h-8 rounded-full flex items-center justify-center">
                        <img src="/static/images/kadosh_logo.png" alt="Kadosh.ia Logo" class="w-8 h-8 rounded-full object-contain">
                    </div>
                    <div class="bg-white dark:bg-gray-800 rounded-lg p-3 max-w-md">
                        <div class="text-gray-900 dark:text-white text-sm">${this.formatMessage(content)}</div>
                        ${source ? `<div class="text-xs text-gray-500 dark:text-gray-400 mt-2">Source: ${this.getSourceLabel(source)}</div>` : ''}
                    </div>
                `;
            }
            
            this.chatMessages.appendChild(messageDiv);
            this.scrollToBottom();
            
            // Save to history
            this.messageHistory.push({
                content,
                sender,
                source,
                timestamp: new Date().toISOString()
            });
            this.saveMessageHistory();
        },
        
        // Format message content (convert markdown-like formatting)
        formatMessage: function(content) {
            // Convert **text** to bold
            content = content.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
            
            // Convert line breaks to <br>
            content = content.replace(/\n/g, '<br>');
            
            // Convert numbered lists
            content = content.replace(/^\d+\.\s/gm, '<br>• ');
            
            // Convert bullet points
            content = content.replace(/^[•·]\s/gm, '<br>• ');
            
            return content;
        },
        
        // Get source label
        getSourceLabel: function(source) {
            const labels = {
                'pre-loaded': 'Base de données biblique',
                'app-help': 'Aide application',
                'openai': 'Intelligence artificielle'
            };
            return labels[source] || source;
        },
        
        // Show loading indicator
        showLoading: function() {
            if (!this.chatMessages) return;
            
            this.isLoading = true;
            
            const loadingDiv = document.createElement('div');
            loadingDiv.className = 'flex items-start space-x-3 loading-message';
            loadingDiv.innerHTML = `
                <div class="w-8 h-8 rounded-full flex items-center justify-center">
                    <img src="/static/images/kadosh_logo.png" alt="Kadosh.ia Logo" class="w-8 h-8 rounded-full object-contain">
                </div>
                <div class="bg-white dark:bg-gray-800 rounded-lg p-3 max-w-md">
                    <div class="flex items-center space-x-2">
                        <div class="spinner"></div>
                        <span class="text-gray-600 dark:text-gray-400 text-sm">Kadosh.ia réfléchit...</span>
                    </div>
                </div>
            `;
            
            this.chatMessages.appendChild(loadingDiv);
            this.scrollToBottom();
            
            // Disable send button
            if (this.sendBtn) {
                this.sendBtn.disabled = true;
                this.sendBtn.classList.add('opacity-50');
            }
        },
        
        // Hide loading indicator
        hideLoading: function() {
            this.isLoading = false;
            
            // Remove loading message
            const loadingMessage = this.chatMessages.querySelector('.loading-message');
            if (loadingMessage) {
                loadingMessage.remove();
            }
            
            // Enable send button
            if (this.sendBtn) {
                this.sendBtn.disabled = false;
                this.sendBtn.classList.remove('opacity-50');
            }
        },
        
        // Scroll to bottom of chat
        scrollToBottom: function() {
            if (this.chatMessages) {
                this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
            }
        },
        
        // Auto-resize input
        autoResizeInput: function() {
            if (this.chatInput) {
                this.chatInput.style.height = 'auto';
                this.chatInput.style.height = this.chatInput.scrollHeight + 'px';
            }
        },
        
        // Escape HTML
        escapeHtml: function(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        },
        
        // Save message history
        saveMessageHistory: function() {
            // Keep only last 50 messages
            const recentHistory = this.messageHistory.slice(-50);
            localStorage.setItem('benj-inside-chat-history', JSON.stringify(recentHistory));
        },
        
        // Load message history
        loadMessageHistory: function() {
            const savedHistory = localStorage.getItem('benj-inside-chat-history');
            if (savedHistory) {
                try {
                    this.messageHistory = JSON.parse(savedHistory);
                } catch (e) {
                    console.error('Error loading chat history:', e);
                    this.messageHistory = [];
                }
            }
        },
        
        // Clear chat history
        clearHistory: function() {
            this.messageHistory = [];
            localStorage.removeItem('benj-inside-chat-history');
            
            // Clear visible messages except welcome message
            if (this.chatMessages) {
                const messages = this.chatMessages.querySelectorAll('.fade-in');
                messages.forEach(msg => {
                    if (!msg.classList.contains('welcome-message')) {
                        msg.remove();
                    }
                });
            }
        }
    };
    
    // Global functions for topic and help buttons
    window.askTopic = function(topic) {
        fetch(`/chatbot/topic/${topic}`)
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    Chatbot.addMessage(`Erreur: ${data.error}`, 'bot', 'error');
                } else {
                    Chatbot.addMessage(`Sujet: ${topic}`, 'user');
                    Chatbot.addMessage(data.response, 'bot', 'pre-loaded');
                }
            })
            .catch(error => {
                console.error('Error asking topic:', error);
                Chatbot.addMessage('Erreur lors de la récupération du sujet', 'bot', 'error');
            });
    };
    
    window.askHelp = function(question) {
        Chatbot.addMessage(question, 'user');
        Chatbot.sendToServer(question);
    };
    
    // Function for selected topic dropdown
    window.askSelectedTopic = function() {
        const dropdown = document.getElementById('topic-dropdown');
        if (dropdown && dropdown.value) {
            const topic = dropdown.value;
            const topicDisplayName = dropdown.options[dropdown.selectedIndex].text;
            
            // Add user message showing selected topic
            Chatbot.addMessage(`Sujet sélectionné: ${topicDisplayName}`, 'user');
            
            // Send topic request
            fetch(`/chatbot/topic/${topic}`)
                .then(response => response.json())
                .then(data => {
                    if (data.error) {
                        Chatbot.addMessage(`Erreur: ${data.error}`, 'bot', 'error');
                    } else {
                        Chatbot.addMessage(data.response, 'bot', 'pre-loaded');
                    }
                })
                .catch(error => {
                    console.error('Error asking topic:', error);
                    Chatbot.addMessage('Erreur lors de la récupération du sujet', 'bot', 'error');
                });
                
            // Reset dropdown
            dropdown.value = '';
        }
    };
    
    // Initialize when DOM is ready
    document.addEventListener('DOMContentLoaded', function() {
        Chatbot.init();
    });
    
    // Export to global scope
    window.Chatbot = Chatbot;
    
})();
