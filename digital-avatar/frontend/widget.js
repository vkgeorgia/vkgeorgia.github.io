/**
 * Valerii Korobeinikov's AI Avatar Widget
 * Embeddable chat widget for GitHub Pages
 */

(function () {
    'use strict';

    // Configuration
    const WIDGET_CONFIG = {
        // Backend URL - Google Cloud Run
        backendUrl: window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
            ? 'http://127.0.0.1:8000'
            : 'https://ai-avatar-103512681014.us-central1.run.app',
        position: 'bottom-right', // bottom-right, bottom-left
        theme: 'dark'
    };

    // Create widget container
    function createWidget() {
        const widgetHTML = `
            <div id="ai-avatar-widget" class="ai-widget-container ai-widget-${WIDGET_CONFIG.position}">
                <button id="ai-widget-toggle" class="ai-widget-toggle" aria-label="Toggle AI Chat">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
                    </svg>
                </button>
                
                <div id="ai-widget-chat" class="ai-widget-chat ai-widget-hidden">
                    <div class="ai-widget-header">
                        <h3>Valerii Korobeinikov's AI Avatar</h3>
                        <div class="ai-widget-status">
                            <span id="ai-widget-status-text">🔄 Connecting...</span>
                        </div>
                        <button id="ai-widget-close" class="ai-widget-close-btn" aria-label="Close chat">×</button>
                    </div>
                    
                    <div id="ai-widget-messages" class="ai-widget-messages">
                        <div class="ai-widget-message ai-widget-message-bot">
                            Hello! I'm Valerii's AI assistant. I can tell you about his professional experience, consulting services, and help schedule a meeting. How can I assist you?
                        </div>
                    </div>
                    
                    <div class="ai-widget-input-area">
                        <input type="text" id="ai-widget-input" placeholder="Type your message..." autocomplete="off">
                        <button id="ai-widget-send" class="ai-widget-send-btn">
                            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                                <line x1="22" y1="2" x2="11" y2="13"></line>
                                <polygon points="22 2 15 22 11 13 2 9 22 2"></polygon>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', widgetHTML);
        initializeWidget();
    }

    // Initialize widget functionality
    function initializeWidget() {
        const toggle = document.getElementById('ai-widget-toggle');
        const chat = document.getElementById('ai-widget-chat');
        const close = document.getElementById('ai-widget-close');
        const input = document.getElementById('ai-widget-input');
        const sendBtn = document.getElementById('ai-widget-send');
        const messagesArea = document.getElementById('ai-widget-messages');
        const statusText = document.getElementById('ai-widget-status-text');

        let socket;
        let isOpen = false;

        // Toggle chat
        toggle.addEventListener('click', () => {
            isOpen = !isOpen;
            chat.classList.toggle('ai-widget-hidden');
            if (isOpen && !socket) {
                connectWebSocket();
            }
        });

        close.addEventListener('click', () => {
            isOpen = false;
            chat.classList.add('ai-widget-hidden');
        });

        // WebSocket connection
        function connectWebSocket() {
            const wsProto = WIDGET_CONFIG.backendUrl.startsWith('https') ? 'wss:' : 'ws:';
            const wsUrl = WIDGET_CONFIG.backendUrl.replace(/^https?:/, wsProto) + '/ws/chat';

            updateStatus('🔄 Connecting...', 'connecting');
            socket = new WebSocket(wsUrl);

            socket.onopen = () => {
                console.log('Connected to AI Avatar');
                updateStatus('✅ AI Active', 'connected');
            };

            socket.onmessage = (event) => {
                const message = event.data;

                if (message.includes('[Offline')) {
                    updateStatus('⚠️ Offline Mode', 'offline');
                } else {
                    updateStatus('✅ AI Active', 'connected');
                }

                addMessage(message, 'bot');
            };

            socket.onclose = () => {
                console.log('Disconnected from AI Avatar');
                updateStatus('❌ Disconnected', 'error');
                setTimeout(connectWebSocket, 3000);
            };

            socket.onerror = (error) => {
                console.error('WebSocket error:', error);
                updateStatus('❌ Connection Error', 'error');
            };
        }

        function updateStatus(text, type) {
            statusText.textContent = text;
            statusText.className = 'ai-widget-status-' + type;
        }

        function parseMarkdown(text) {
            return text
                .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
                .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank">$1</a>')
                .replace(/^[\*\-] (.+)$/gm, '<li>$1</li>')
                .replace(/(<li>.*<\/li>\s*)+/gs, '<ul>$&</ul>')
                .replace(/\n/g, '<br>');
        }

        function addMessage(text, sender) {
            const div = document.createElement('div');
            div.classList.add('ai-widget-message', `ai-widget-message-${sender}`);

            if (sender === 'bot') {
                div.innerHTML = parseMarkdown(text);
            } else {
                div.textContent = text;
            }

            messagesArea.appendChild(div);
            messagesArea.scrollTop = messagesArea.scrollHeight;
        }

        function sendMessage() {
            const text = input.value.trim();
            if (!text) return;

            addMessage(text, 'user');

            if (socket && socket.readyState === WebSocket.OPEN) {
                socket.send(text);
            } else {
                addMessage('Error: Connection lost', 'bot');
            }

            input.value = '';
        }

        sendBtn.addEventListener('click', sendMessage);
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    // Load CSS
    function loadStyles() {
        // CSS is now loaded directly in the HTML layout
        // This function is kept for backward compatibility
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            createWidget();
        });
    } else {
        createWidget();
    }
})();
