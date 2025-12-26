document.addEventListener('DOMContentLoaded', () => {
    const input = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const messagesArea = document.getElementById('chat-messages');
    const statusBar = document.getElementById('status-bar');
    const statusText = document.getElementById('status-text');

    function updateStatus(message, type = 'normal') {
        statusText.textContent = message;
        statusBar.className = 'status-bar ' + type;
    }

    // Dynamic Base URL
    const protocol = window.location.protocol;
    const hostname = window.location.hostname;
    const port = window.location.port ? `:${window.location.port}` : '';

    // Connect to WebSocket
    const wsProto = protocol === 'https:' ? 'wss:' : 'ws:';
    const wsUrl = `${wsProto}//${hostname}${port}/ws/chat`;

    let socket;

    function connectWebSocket() {
        updateStatus('🔄 Connecting...', 'normal');
        socket = new WebSocket(wsUrl);

        socket.onopen = () => {
            console.log('Connected to WebSocket');
            updateStatus('✅ Connected | AI Ready', 'connected');
        };

        socket.onmessage = (event) => {
            const message = event.data;

            // Detect offline mode
            if (message.includes('[Offline')) {
                updateStatus('⚠️ Offline Mode | Local Search', 'offline');
            } else {
                updateStatus('✅ AI Active', 'connected');
            }

            addMessage(message, 'bot');
        };

        socket.onclose = () => {
            console.log('WebSocket disconnected. Retrying in 3s...');
            updateStatus('❌ Disconnected | Reconnecting...', 'error');
            setTimeout(connectWebSocket, 3000);
        };

        socket.onerror = (error) => {
            console.error('WebSocket error:', error);
            updateStatus('❌ Connection Error', 'error');
        };
    }

    try {
        connectWebSocket();
    } catch (e) {
        console.error("Failed to connect to WS", e);
    }

    // UI Functions
    function parseMarkdown(text) {
        // Simple markdown parser
        return text
            // Bold (must come before italic)
            .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
            // Links
            .replace(/\[(.+?)\]\((.+?)\)/g, '<a href="$2" target="_blank">$1</a>')
            // Bullet points (both * and -)
            .replace(/^[\*\-] (.+)$/gm, '<li>$1</li>')
            // Wrap lists
            .replace(/(<li>.*<\/li>\s*)+/gs, '<ul>$&</ul>')
            // Line breaks
            .replace(/\n/g, '<br>');
    }

    function addMessage(text, sender) {
        const div = document.createElement('div');
        div.classList.add('message', sender);

        if (sender === 'bot') {
            // Render markdown for bot messages
            div.innerHTML = parseMarkdown(text);
        } else {
            // Plain text for user messages
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
            console.warn('Socket not connected');
            addMessage('Error: Connection lost', 'bot');
        }

        input.value = '';
    }

    // Event Listeners
    sendBtn.addEventListener('click', sendMessage);

    input.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendMessage();
        }
    });
});
