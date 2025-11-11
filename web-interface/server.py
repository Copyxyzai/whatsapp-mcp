"""
FastAPI Web Interface for WhatsApp MCP Server
Provides REST API endpoints to interact with WhatsApp functionality
"""

from fastapi import FastAPI, HTTPException, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import sys
import os

# Add parent directory to path to import whatsapp modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'whatsapp-mcp-server'))

from whatsapp import (
    search_contacts as whatsapp_search_contacts,
    list_messages as whatsapp_list_messages,
    list_chats as whatsapp_list_chats,
    get_chat as whatsapp_get_chat,
    get_direct_chat_by_contact as whatsapp_get_direct_chat_by_contact,
    get_contact_chats as whatsapp_get_contact_chats,
    get_last_interaction as whatsapp_get_last_interaction,
    get_message_context as whatsapp_get_message_context,
    send_message as whatsapp_send_message,
    send_file as whatsapp_send_file,
    send_audio_message as whatsapp_audio_voice_message,
    download_media as whatsapp_download_media
)

# Initialize FastAPI app
app = FastAPI(
    title="WhatsApp MCP Web Interface",
    description="REST API for WhatsApp MCP Server",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response Models
class SearchContactsRequest(BaseModel):
    query: str

class ListMessagesRequest(BaseModel):
    after: Optional[str] = None
    before: Optional[str] = None
    sender_phone_number: Optional[str] = None
    chat_jid: Optional[str] = None
    query: Optional[str] = None
    limit: int = 20
    page: int = 0
    include_context: bool = True
    context_before: int = 1
    context_after: int = 1

class ListChatsRequest(BaseModel):
    query: Optional[str] = None
    limit: int = 20
    page: int = 0
    include_last_message: bool = True
    sort_by: str = "last_active"

class GetChatRequest(BaseModel):
    chat_jid: str
    include_last_message: bool = True

class GetDirectChatByContactRequest(BaseModel):
    sender_phone_number: str

class GetContactChatsRequest(BaseModel):
    jid: str
    limit: int = 20
    page: int = 0

class GetLastInteractionRequest(BaseModel):
    jid: str

class GetMessageContextRequest(BaseModel):
    message_id: str
    before: int = 5
    after: int = 5

class SendMessageRequest(BaseModel):
    recipient: str
    message: str

class SendFileRequest(BaseModel):
    recipient: str
    media_path: str

class SendAudioMessageRequest(BaseModel):
    recipient: str
    media_path: str

class DownloadMediaRequest(BaseModel):
    message_id: str
    chat_jid: str

# API Endpoints
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "WhatsApp MCP Web Interface API",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.post("/api/contacts/search")
async def search_contacts(request: SearchContactsRequest) -> List[Dict[str, Any]]:
    """Search WhatsApp contacts by name or phone number"""
    try:
        contacts = whatsapp_search_contacts(request.query)
        return contacts
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages/list")
async def list_messages(request: ListMessagesRequest) -> List[Dict[str, Any]]:
    """Get WhatsApp messages matching specified criteria with optional context"""
    try:
        messages = whatsapp_list_messages(
            after=request.after,
            before=request.before,
            sender_phone_number=request.sender_phone_number,
            chat_jid=request.chat_jid,
            query=request.query,
            limit=request.limit,
            page=request.page,
            include_context=request.include_context,
            context_before=request.context_before,
            context_after=request.context_after
        )
        return messages
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chats/list")
async def list_chats(request: ListChatsRequest) -> List[Dict[str, Any]]:
    """Get WhatsApp chats matching specified criteria"""
    try:
        chats = whatsapp_list_chats(
            query=request.query,
            limit=request.limit,
            page=request.page,
            include_last_message=request.include_last_message,
            sort_by=request.sort_by
        )
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chats/get")
async def get_chat(request: GetChatRequest) -> Dict[str, Any]:
    """Get WhatsApp chat metadata by JID"""
    try:
        chat = whatsapp_get_chat(request.chat_jid, request.include_last_message)
        return chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chats/get-by-contact")
async def get_direct_chat_by_contact(request: GetDirectChatByContactRequest) -> Dict[str, Any]:
    """Get WhatsApp chat metadata by sender phone number"""
    try:
        chat = whatsapp_get_direct_chat_by_contact(request.sender_phone_number)
        return chat
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chats/get-contact-chats")
async def get_contact_chats(request: GetContactChatsRequest) -> List[Dict[str, Any]]:
    """Get all WhatsApp chats involving the contact"""
    try:
        chats = whatsapp_get_contact_chats(request.jid, request.limit, request.page)
        return chats
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/interactions/get-last")
async def get_last_interaction(request: GetLastInteractionRequest) -> str:
    """Get most recent WhatsApp message involving the contact"""
    try:
        message = whatsapp_get_last_interaction(request.jid)
        return message
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages/get-context")
async def get_message_context(request: GetMessageContextRequest) -> Dict[str, Any]:
    """Get context around a specific WhatsApp message"""
    try:
        context = whatsapp_get_message_context(request.message_id, request.before, request.after)
        return context
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/messages/send")
async def send_message(request: SendMessageRequest) -> Dict[str, Any]:
    """Send a WhatsApp message to a person or group"""
    try:
        if not request.recipient:
            raise HTTPException(status_code=400, detail="Recipient must be provided")
        
        success, status_message = whatsapp_send_message(request.recipient, request.message)
        return {
            "success": success,
            "message": status_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/files/send")
async def send_file(request: SendFileRequest) -> Dict[str, Any]:
    """Send a file via WhatsApp to the specified recipient"""
    try:
        success, status_message = whatsapp_send_file(request.recipient, request.media_path)
        return {
            "success": success,
            "message": status_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/audio/send")
async def send_audio_message(request: SendAudioMessageRequest) -> Dict[str, Any]:
    """Send an audio file as a WhatsApp audio message"""
    try:
        success, status_message = whatsapp_audio_voice_message(request.recipient, request.media_path)
        return {
            "success": success,
            "message": status_message
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/media/download")
async def download_media(request: DownloadMediaRequest) -> Dict[str, Any]:
    """Download media from a WhatsApp message and get the local file path"""
    try:
        file_path = whatsapp_download_media(request.message_id, request.chat_jid)
        
        if file_path:
            return {
                "success": True,
                "message": "Media downloaded successfully",
                "file_path": file_path
            }
        else:
            return {
                "success": False,
                "message": "Failed to download media"
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
