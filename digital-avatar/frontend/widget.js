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
                        <button id="ai-widget-close" class="ai-widget-close-btn" aria-label="Close chat">×</button>
                        <h3>Ask Valerii</h3>
                        <p class="ai-widget-subtitle">AI-powered assistant</p>
                        <div class="ai-widget-status">
                            <span id="ai-widget-status-text" class="ai-widget-status-connecting">● AI</span>
                            <span class="ai-widget-status-divider">|</span>
                            <span id="ai-widget-db-status-text" class="ai-widget-status-connecting">● DB</span>
                        </div>
                    </div>
                    
                    <div id="ai-widget-messages" class="ai-widget-messages">
                        <div class="ai-widget-message ai-widget-message-bot">
                            Hi! I'm Valerii's AI assistant. Here's what I can do:<br><br>
                            <strong>1. Experience &amp; approach</strong> — projects, industries, domains, professional philosophy.<br>
                            <strong>2. Schedule a meeting</strong> — book a call directly in Valerii's calendar.<br>
                            <strong>3. Tailored resume</strong> — share a vacancy and I'll generate a resume focused on what matters for that role.<br>
                            <strong>4. Forward a link</strong> — drop a vacancy URL or your company site and I'll pass it to Valerii directly.<br><br>
                            What brings you here?
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
        const dbStatusText = document.getElementById('ai-widget-db-status-text');

        let socket;
        let isOpen = false;
        let reconnectAttempts = 0;
        const MAX_RECONNECT_ATTEMPTS = 5;
        const MAX_MESSAGE_LENGTH = 8000; // raised to allow job vacancy texts for resume generation

        function escapeHtml(str) {
            return str
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;');
        }

        // Toggle chat — hide/show the round button when chat opens/closes
        toggle.addEventListener('click', () => {
            isOpen = !isOpen;
            chat.classList.toggle('ai-widget-hidden');
            toggle.classList.toggle('ai-widget-toggle-hidden', isOpen);
            if (isOpen && !socket) {
                connectWebSocket();
                checkDbStatus();
            }
        });

        close.addEventListener('click', () => {
            isOpen = false;
            chat.classList.add('ai-widget-hidden');
            toggle.classList.remove('ai-widget-toggle-hidden');
        });

        // WebSocket connection
        function connectWebSocket() {
            const wsProto = WIDGET_CONFIG.backendUrl.startsWith('https') ? 'wss:' : 'ws:';
            const wsUrl = WIDGET_CONFIG.backendUrl.replace(/^https?:/, wsProto) + '/ws/chat';

            updateStatus('🔄 Connecting...', 'connecting');
            socket = new WebSocket(wsUrl);

            socket.onopen = () => {
                reconnectAttempts = 0;
                updateStatus('● AI', 'connected');
            };

            socket.onmessage = (event) => {
                const message = event.data;
                updateStatus(message.includes('[Offline') ? '● AI' : '● AI',
                             message.includes('[Offline') ? 'offline' : 'connected');
                addMessage(message, 'bot');
            };

            socket.onclose = () => {
                if (reconnectAttempts < MAX_RECONNECT_ATTEMPTS) {
                    const delay = Math.min(1000 * Math.pow(2, reconnectAttempts), 30000);
                    reconnectAttempts++;
                    updateStatus('● AI', 'connecting');
                    setTimeout(connectWebSocket, delay);
                } else {
                    updateStatus('● AI', 'error');
                }
            };

            socket.onerror = () => {
                updateStatus('● AI', 'error');
            };
        }

        function updateStatus(text, type) {
            statusText.textContent = text;
            statusText.className = 'ai-widget-status-' + type;
        }

        async function checkDbStatus() {
            try {
                const resp = await fetch(WIDGET_CONFIG.backendUrl + '/api/health');
                const data = await resp.json();
                if (data.db && data.db.ok) {
                    dbStatusText.textContent = '● DB';
                    dbStatusText.className = 'ai-widget-status-connected';
                } else {
                    dbStatusText.textContent = '● DB';
                    dbStatusText.className = 'ai-widget-status-error';
                }
            } catch (_) {
                dbStatusText.textContent = '● DB';
                dbStatusText.className = 'ai-widget-status-error';
            }
        }

        function parseMarkdown(text) {
            // Escape HTML first to prevent XSS
            let t = escapeHtml(text);

            // Bold: **text**
            t = t.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');

            // Markdown links: [label](https://...)
            t = t.replace(
                /\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)/g,
                '<a href="$2" target="_blank" rel="noopener noreferrer" style="color:#4a9eff;text-decoration:underline">$1</a>'
            );

            // Plain URLs not already inside an href attribute
            t = t.replace(
                /(?<!href=")(https?:\/\/[^\s&<>"]+)/g,
                '<a href="$1" target="_blank" rel="noopener noreferrer" style="color:#4a9eff;text-decoration:underline">$1</a>'
            );

            // List items
            t = t.replace(/^[*\-] (.+)$/gm, '<li>$1</li>');
            t = t.replace(/(<li>[\s\S]*?<\/li>)+/g, '<ul>$&</ul>');

            // Newlines
            t = t.replace(/\n/g, '<br>');

            return t;
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

            if (text.length > MAX_MESSAGE_LENGTH) {
                addMessage(`Message is too long (max ${MAX_MESSAGE_LENGTH} characters).`, 'bot');
                return;
            }

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
