// Global state
let currentChatJid = null;
let allChats = [];

// Initialize the application
document.addEventListener('DOMContentLoaded', function() {
    loadChats();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    // Refresh chats button
    document.getElementById('refreshChatsBtn').addEventListener('click', loadChats);
    
    // Refresh messages button
    document.getElementById('refreshMessagesBtn').addEventListener('click', function() {
        if (currentChatJid) {
            loadMessages(currentChatJid);
        }
    });
    
    // Message form submission
    document.getElementById('messageForm').addEventListener('submit', function(e) {
        e.preventDefault();
        sendMessage();
    });
    
    // Search chats
    document.getElementById('searchChats').addEventListener('input', function(e) {
        filterChats(e.target.value);
    });
}

// Load chats from API
async function loadChats() {
    const chatsList = document.getElementById('chatsList');
    chatsList.innerHTML = '<div class="loading">Loading chats...</div>';
    
    try {
        const response = await fetch('/api/chats?limit=100');
        const data = await response.json();
        
        if (data.success) {
            allChats = data.chats;
            displayChats(allChats);
        } else {
            chatsList.innerHTML = `<div class="error">Error: ${data.error}</div>`;
        }
    } catch (error) {
        chatsList.innerHTML = `<div class="error">Failed to load chats: ${error.message}</div>`;
    }
}

// Display chats in the sidebar
function displayChats(chats) {
    const chatsList = document.getElementById('chatsList');
    
    if (chats.length === 0) {
        chatsList.innerHTML = '<div class="loading">No chats found</div>';
        return;
    }
    
    chatsList.innerHTML = '';
    
    chats.forEach(chat => {
        const chatItem = createChatElement(chat);
        chatsList.appendChild(chatItem);
    });
}

// Create a chat element
function createChatElement(chat) {
    const div = document.createElement('div');
    div.className = 'chat-item';
    if (chat.jid === currentChatJid) {
        div.classList.add('active');
    }
    
    // Format timestamp
    const time = chat.last_message_time ? formatTime(chat.last_message_time) : '';
    
    // Create preview text
    let preview = chat.last_message || 'No messages yet';
    if (chat.media_type) {
        preview = `📎 ${chat.media_type}`;
    }
    if (chat.last_is_from_me) {
        preview = 'You: ' + preview;
    }
    
    div.innerHTML = `
        <div class="chat-item-header">
            <span class="chat-item-name">
                ${escapeHtml(chat.name)}
                ${chat.is_group ? '<span class="chat-item-badge">Group</span>' : ''}
            </span>
            <span class="chat-item-time">${time}</span>
        </div>
        <div class="chat-item-preview ${chat.media_type ? 'media' : ''}">
            ${escapeHtml(preview.substring(0, 50))}${preview.length > 50 ? '...' : ''}
        </div>
    `;
    
    div.addEventListener('click', () => selectChat(chat));
    
    return div;
}

// Select a chat
function selectChat(chat) {
    currentChatJid = chat.jid;
    
    // Update UI
    document.getElementById('welcomeScreen').style.display = 'none';
    document.getElementById('chatScreen').style.display = 'flex';
    document.getElementById('chatName').textContent = chat.name;
    document.getElementById('chatJid').textContent = chat.jid;
    
    // Update active state in sidebar
    document.querySelectorAll('.chat-item').forEach(item => {
        item.classList.remove('active');
    });
    event.currentTarget.classList.add('active');
    
    // Load messages
    loadMessages(chat.jid);
}

// Load messages for a chat
async function loadMessages(chatJid) {
    const messagesArea = document.getElementById('messagesArea');
    messagesArea.innerHTML = '<div class="loading">Loading messages...</div>';
    
    try {
        const response = await fetch(`/api/messages/${encodeURIComponent(chatJid)}?limit=100`);
        const data = await response.json();
        
        if (data.success) {
            displayMessages(data.messages);
        } else {
            messagesArea.innerHTML = `<div class="error">Error: ${data.error}</div>`;
        }
    } catch (error) {
        messagesArea.innerHTML = `<div class="error">Failed to load messages: ${error.message}</div>`;
    }
}

// Display messages
function displayMessages(messages) {
    const messagesArea = document.getElementById('messagesArea');
    
    if (messages.length === 0) {
        messagesArea.innerHTML = '<div class="loading">No messages in this chat</div>';
        return;
    }
    
    messagesArea.innerHTML = '';
    
    messages.forEach(message => {
        const messageElement = createMessageElement(message);
        messagesArea.appendChild(messageElement);
    });
    
    // Scroll to bottom
    messagesArea.scrollTop = messagesArea.scrollHeight;
}

// Create a message element
function createMessageElement(message) {
    const div = document.createElement('div');
    div.className = `message ${message.is_from_me ? 'sent' : 'received'}`;
    
    let content = '';
    
    // Add sender name for group chats or received messages
    if (!message.is_from_me && currentChatJid && currentChatJid.endsWith('@g.us')) {
        content += `<div class="message-sender">${escapeHtml(message.sender)}</div>`;
    }
    
    // Add message content
    if (message.content) {
        content += `<div class="message-content">${escapeHtml(message.content)}</div>`;
    }
    
    // Add media indicator
    if (message.media_type) {
        content += `<div class="message-media">📎 ${escapeHtml(message.media_type)}: ${escapeHtml(message.filename || 'file')}</div>`;
    }
    
    // Add timestamp
    const time = formatTime(message.timestamp);
    content += `<div class="message-time">${time}</div>`;
    
    div.innerHTML = content;
    
    return div;
}

// Send a message
async function sendMessage() {
    if (!currentChatJid) {
        alert('Please select a chat first');
        return;
    }
    
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message) {
        return;
    }
    
    // Disable input while sending
    messageInput.disabled = true;
    
    try {
        const response = await fetch('/api/send', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                recipient: currentChatJid,
                message: message
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Clear input
            messageInput.value = '';
            
            // Add message to UI immediately
            const messagesArea = document.getElementById('messagesArea');
            const messageElement = createMessageElement({
                id: 'temp-' + Date.now(),
                chat_jid: currentChatJid,
                sender: 'You',
                content: message,
                timestamp: new Date().toISOString(),
                is_from_me: true,
                media_type: null,
                filename: null
            });
            messagesArea.appendChild(messageElement);
            messagesArea.scrollTop = messagesArea.scrollHeight;
            
            // Reload messages after a short delay to get the real message
            setTimeout(() => loadMessages(currentChatJid), 1000);
        } else {
            alert(`Failed to send message: ${data.error || data.message}`);
        }
    } catch (error) {
        alert(`Failed to send message: ${error.message}`);
    } finally {
        messageInput.disabled = false;
        messageInput.focus();
    }
}

// Filter chats by search query
function filterChats(query) {
    const filtered = allChats.filter(chat => {
        const searchText = query.toLowerCase();
        return chat.name.toLowerCase().includes(searchText) ||
               chat.jid.toLowerCase().includes(searchText) ||
               (chat.last_message && chat.last_message.toLowerCase().includes(searchText));
    });
    
    displayChats(filtered);
}

// Format timestamp
function formatTime(timestamp) {
    if (!timestamp) return '';
    
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now - date;
    
    // Today
    if (diff < 86400000 && date.getDate() === now.getDate()) {
        return date.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
    }
    
    // Yesterday
    const yesterday = new Date(now);
    yesterday.setDate(yesterday.getDate() - 1);
    if (date.getDate() === yesterday.getDate() && 
        date.getMonth() === yesterday.getMonth() && 
        date.getFullYear() === yesterday.getFullYear()) {
        return 'Yesterday';
    }
    
    // This year
    if (date.getFullYear() === now.getFullYear()) {
        return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
    }
    
    // Other years
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    if (!text) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Auto-refresh chats every 30 seconds
setInterval(() => {
    if (document.visibilityState === 'visible') {
        loadChats();
        if (currentChatJid) {
            loadMessages(currentChatJid);
        }
    }
}, 30000);
