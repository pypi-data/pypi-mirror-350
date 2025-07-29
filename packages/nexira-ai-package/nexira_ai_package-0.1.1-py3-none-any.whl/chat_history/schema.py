from pydantic import BaseModel
from typing import  List, Optional, Dict, Any
import json
from datetime import datetime

class ChatHistoryRequest(BaseModel):
    user_id: str
    chat_id: str

class MessageRequest(BaseModel):
    timestamp: datetime
    message_id: int
    role: str
    content: str

class UserThread(BaseModel):
    user_id: int
    chat_id: int
    agent_name: str

class ConversationInfor(BaseModel):
    user_thread: UserThread
    messages: List[MessageRequest]
