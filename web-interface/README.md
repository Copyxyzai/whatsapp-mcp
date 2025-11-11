# WhatsApp MCP Web Interface

This is a FastAPI-based web interface for the WhatsApp MCP Server. It provides REST API endpoints to interact with WhatsApp functionality through HTTP requests.

## Features

- RESTful API endpoints for all WhatsApp MCP tools
- Interactive API documentation (Swagger UI)
- CORS support for web applications
- JSON request/response format
- Easy integration with web and mobile applications

## Installation

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

   Or using uv:

   ```bash
   uv pip install -r requirements.txt
   ```

2. **Make sure the WhatsApp bridge is running**

   Navigate to the whatsapp-bridge directory and run:

   ```bash
   cd ../whatsapp-bridge
   go run main.go
   ```

## Running the Server

Start the FastAPI server:

```bash
python server.py
```

Or with uvicorn directly:

```bash
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```

The server will start on `http://localhost:8000`

### Demo Interface

A demo HTML interface is included at `demo.html`. To use it:

1. Start the FastAPI server (see above)
2. Open `demo.html` in your web browser
3. The demo provides a simple UI to:
   - Send messages
   - Search contacts
   - List recent messages

Note: For the demo to work, you may need to serve it through the FastAPI server or enable CORS in your browser.

## API Documentation

Once the server is running, you can access:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative API docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

## Available Endpoints

### Contacts
- `POST /api/contacts/search` - Search contacts by name or phone number

### Messages
- `POST /api/messages/list` - List messages with filters
- `POST /api/messages/send` - Send a message
- `POST /api/messages/get-context` - Get context around a message

### Chats
- `POST /api/chats/list` - List chats
- `POST /api/chats/get` - Get chat by JID
- `POST /api/chats/get-by-contact` - Get chat by contact phone number
- `POST /api/chats/get-contact-chats` - Get all chats for a contact

### Interactions
- `POST /api/interactions/get-last` - Get last interaction with a contact

### Media
- `POST /api/files/send` - Send a file (image, video, document)
- `POST /api/audio/send` - Send an audio message
- `POST /api/media/download` - Download media from a message

### Health
- `GET /api/health` - Health check endpoint

## Example Usage

### Search Contacts

```bash
curl -X POST "http://localhost:8000/api/contacts/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "John"}'
```

### Send a Message

```bash
curl -X POST "http://localhost:8000/api/messages/send" \
  -H "Content-Type: application/json" \
  -d '{"recipient": "1234567890", "message": "Hello from the API!"}'
```

### List Messages

```bash
curl -X POST "http://localhost:8000/api/messages/list" \
  -H "Content-Type: application/json" \
  -d '{"limit": 10, "page": 0}'
```

## Security Considerations

⚠️ **Important**: This web interface exposes your WhatsApp functionality over HTTP. In production:

1. Use HTTPS/TLS encryption
2. Implement authentication and authorization
3. Configure CORS appropriately (don't use `allow_origins=["*"]`)
4. Use environment variables for sensitive configuration
5. Consider rate limiting to prevent abuse
6. Run behind a reverse proxy (nginx, Apache, etc.)

## Development

For development with auto-reload:

```bash
uvicorn server:app --reload --host 0.0.0.0 --port 8000
```

## Troubleshooting

- **Cannot import whatsapp modules**: Make sure the WhatsApp bridge is set up and the database exists
- **CORS errors**: Update the CORS configuration in `server.py`
- **Connection refused**: Ensure the WhatsApp bridge is running and the database is accessible

## Integration with Frontend

You can now build a web or mobile frontend that communicates with this API. Example frameworks:

- **React/Vue/Angular** for web applications
- **React Native/Flutter** for mobile applications
- **Electron** for desktop applications

All endpoints accept and return JSON, making integration straightforward.
