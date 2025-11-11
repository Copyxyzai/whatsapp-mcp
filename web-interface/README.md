# WhatsApp MCP - Web Interface

A web-based interface for the WhatsApp MCP application, allowing you to access your WhatsApp messages through a browser.

## Features

- 📱 View all your WhatsApp chats in a clean, modern interface
- 💬 Read and send messages
- 🔍 Search through chats
- 🎨 WhatsApp-like UI design
- 🔄 Auto-refresh messages
- 👥 Support for both individual and group chats
- 📎 Media message indicators

## Prerequisites

Before running the web interface, make sure you have:

1. **WhatsApp Bridge running**: The Go WhatsApp bridge must be running on port 8080
   ```bash
   cd ../whatsapp-bridge
   go run main.go
   ```

2. **Python 3.6+** installed on your system

3. **WhatsApp authenticated**: You must have already scanned the QR code and authenticated your WhatsApp account

## Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

   Or using uv (recommended):
   ```bash
   uv pip install -r requirements.txt
   ```

## Running the Web Interface

1. **Start the WhatsApp bridge** (in a separate terminal):
   ```bash
   cd ../whatsapp-bridge
   go run main.go
   ```

2. **Start the web interface**:
   ```bash
   python app.py
   ```

3. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## Usage

1. **View Chats**: All your chats appear in the left sidebar, sorted by most recent activity
2. **Select a Chat**: Click on any chat to view its messages
3. **Send Messages**: Type your message in the input field at the bottom and press Enter or click Send
4. **Search**: Use the search box at the top of the sidebar to filter chats
5. **Refresh**: Click the refresh button (↻) to manually update chats or messages

## Security Notes

⚠️ **Important Security Considerations**:

- This web interface runs on your local machine and is intended for personal use
- By default, it binds to `0.0.0.0:5000`, making it accessible on your local network
- For production use, you should:
  - Add authentication (username/password)
  - Use HTTPS (SSL/TLS)
  - Add rate limiting
  - Implement proper session management
  - Consider using a reverse proxy (nginx, Apache)
  
- **Do NOT expose this directly to the internet without proper security measures**

## Architecture

The web interface consists of:

1. **Flask Backend** (`app.py`): Serves the web interface and provides REST API endpoints
2. **HTML Template** (`templates/index.html`): Single-page application structure
3. **CSS** (`static/css/style.css`): WhatsApp-inspired styling
4. **JavaScript** (`static/js/app.js`): Client-side logic for chat interaction

### API Endpoints

- `GET /api/chats` - Get all chats
- `GET /api/messages/<chat_jid>` - Get messages for a specific chat
- `POST /api/send` - Send a message
- `GET /api/contacts` - Search contacts
- `POST /api/download/<message_id>` - Download media from a message

## Customization

### Changing the Port

Edit `app.py` and modify the last line:

```python
app.run(host='0.0.0.0', port=5000, debug=True)
```

Change `port=5000` to your desired port number.

### Adding Authentication

For basic authentication, you can add Flask-HTTPAuth:

```bash
pip install Flask-HTTPAuth
```

Then modify `app.py` to require authentication for all routes.

## Troubleshooting

### "Failed to connect to WhatsApp bridge"
- Make sure the Go WhatsApp bridge is running on port 8080
- Check that the `WHATSAPP_API_BASE_URL` in `app.py` matches your bridge configuration

### "Database locked" errors
- The SQLite database might be locked by another process
- Make sure only one instance of the application is accessing the database

### Messages not appearing
- Wait a few seconds for messages to sync
- Click the refresh button (↻)
- Check that the WhatsApp bridge is connected and authenticated

### "No chats found"
- Make sure you have sent/received messages in WhatsApp
- Verify that the WhatsApp bridge has synced your message history
- Check the database path in `app.py` matches your actual database location

## Development

To run in development mode with auto-reload:

```bash
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
```

## License

This web interface is part of the WhatsApp MCP project and follows the same license terms.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.
