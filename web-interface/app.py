"""
WhatsApp MCP Web Interface
A web-based interface for the WhatsApp MCP application
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import sqlite3
import os
import requests
from datetime import datetime
from typing import List, Dict, Any, Optional

app = Flask(__name__)

# Configuration
MESSAGES_DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'whatsapp-bridge', 'store', 'messages.db')
WHATSAPP_API_BASE_URL = "http://localhost:8080/api"

def get_db_connection():
    """Create a database connection."""
    conn = sqlite3.connect(MESSAGES_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """Serve the main page."""
    return render_template('index.html')

@app.route('/api/chats', methods=['GET'])
def get_chats():
    """Get all chats."""
    try:
        limit = int(request.args.get('limit', 50))
        page = int(request.args.get('page', 0))
        offset = page * limit
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get chats with their last message
        cursor.execute("""
            SELECT 
                c.jid,
                c.name,
                c.last_message_time,
                m.content as last_message,
                m.sender as last_sender,
                m.is_from_me as last_is_from_me,
                m.media_type
            FROM chats c
            LEFT JOIN messages m ON c.jid = m.chat_jid 
                AND m.timestamp = c.last_message_time
            ORDER BY c.last_message_time DESC
            LIMIT ? OFFSET ?
        """, (limit, offset))
        
        chats = []
        for row in cursor.fetchall():
            chat = {
                'jid': row['jid'],
                'name': row['name'] or row['jid'],
                'last_message_time': row['last_message_time'],
                'last_message': row['last_message'] or '',
                'last_sender': row['last_sender'],
                'last_is_from_me': bool(row['last_is_from_me']),
                'media_type': row['media_type'],
                'is_group': row['jid'].endswith('@g.us')
            }
            chats.append(chat)
        
        conn.close()
        return jsonify({'success': True, 'chats': chats})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/messages/<chat_jid>', methods=['GET'])
def get_messages(chat_jid):
    """Get messages for a specific chat."""
    try:
        limit = int(request.args.get('limit', 50))
        page = int(request.args.get('page', 0))
        offset = page * limit
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get messages for the chat
        cursor.execute("""
            SELECT 
                id,
                chat_jid,
                sender,
                content,
                timestamp,
                is_from_me,
                media_type,
                filename
            FROM messages
            WHERE chat_jid = ?
            ORDER BY timestamp DESC
            LIMIT ? OFFSET ?
        """, (chat_jid, limit, offset))
        
        messages = []
        for row in cursor.fetchall():
            message = {
                'id': row['id'],
                'chat_jid': row['chat_jid'],
                'sender': row['sender'],
                'content': row['content'] or '',
                'timestamp': row['timestamp'],
                'is_from_me': bool(row['is_from_me']),
                'media_type': row['media_type'],
                'filename': row['filename']
            }
            messages.append(message)
        
        # Reverse to show oldest first
        messages.reverse()
        
        conn.close()
        return jsonify({'success': True, 'messages': messages})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/send', methods=['POST'])
def send_message():
    """Send a message via the WhatsApp bridge API."""
    try:
        data = request.json
        recipient = data.get('recipient')
        message = data.get('message', '')
        
        if not recipient:
            return jsonify({'success': False, 'error': 'Recipient is required'}), 400
        
        if not message:
            return jsonify({'success': False, 'error': 'Message is required'}), 400
        
        # Call the WhatsApp bridge API
        response = requests.post(
            f'{WHATSAPP_API_BASE_URL}/send',
            json={
                'recipient': recipient,
                'message': message
            },
            timeout=10
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify(result)
        else:
            return jsonify({
                'success': False,
                'error': f'API returned status {response.status_code}'
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Failed to connect to WhatsApp bridge: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/contacts', methods=['GET'])
def search_contacts():
    """Search contacts."""
    try:
        query = request.args.get('query', '').lower()
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Search in chats for contacts (non-group chats)
        if query:
            cursor.execute("""
                SELECT DISTINCT jid, name
                FROM chats
                WHERE jid LIKE '%@s.whatsapp.net'
                AND (LOWER(name) LIKE ? OR jid LIKE ?)
                ORDER BY name
                LIMIT 50
            """, (f'%{query}%', f'%{query}%'))
        else:
            cursor.execute("""
                SELECT DISTINCT jid, name
                FROM chats
                WHERE jid LIKE '%@s.whatsapp.net'
                ORDER BY name
                LIMIT 50
            """)
        
        contacts = []
        for row in cursor.fetchall():
            contact = {
                'jid': row['jid'],
                'name': row['name'] or row['jid'].split('@')[0],
                'phone_number': row['jid'].split('@')[0]
            }
            contacts.append(contact)
        
        conn.close()
        return jsonify({'success': True, 'contacts': contacts})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/download/<message_id>', methods=['POST'])
def download_media(message_id):
    """Download media from a message."""
    try:
        data = request.json
        chat_jid = data.get('chat_jid')
        
        if not chat_jid:
            return jsonify({'success': False, 'error': 'chat_jid is required'}), 400
        
        # Call the WhatsApp bridge API
        response = requests.post(
            f'{WHATSAPP_API_BASE_URL}/download',
            json={
                'message_id': message_id,
                'chat_jid': chat_jid
            },
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            return jsonify(result)
        else:
            return jsonify({
                'success': False,
                'error': f'API returned status {response.status_code}'
            }), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({
            'success': False,
            'error': f'Failed to connect to WhatsApp bridge: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    # Run the Flask app
    app.run(host='0.0.0.0', port=5000, debug=True)
