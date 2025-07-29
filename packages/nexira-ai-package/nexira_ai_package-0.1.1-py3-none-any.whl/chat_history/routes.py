from fastapi import APIRouter, HTTPException, FastAPI
from .memory_handler import MemoryHandler
from .schema import UserThread, ConversationInfor
from contextlib import asynccontextmanager

#mongo_db_client = MongoDBClient(app_config.MONGODB_URI)
mongo_db_client = MemoryHandler("chat_history", "chat_history")

@asynccontextmanager
async def lifespan(app: FastAPI):
    await mongo_db_client.connect_to_database()
    print("🔌 MongoDB connected at startup")
    yield
    await mongo_db_client.close_connection()
    print("🔒 MongoDB disconnected at shutdown")

router = APIRouter(
    prefix="/chat",
    tags=["chat"]
)

@router.get("/get_all_users")
async def get_all_users():
    try:
        users = await mongo_db_client.get_all_users()
        return {"users": users}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/clear_chat")
async def clear_chat(user_thread: UserThread):
    try:
        await mongo_db_client.clear_conversation(user_thread)
        return {"message": "Chat cleared successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.get("/get_all_chats/{user_id}")
async def get_all_chats(user_id: int):
    try:
        chats = await mongo_db_client.get_all_chats(user_id)
        return {"chats": chats}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@router.get("/chat_history/{user_id}/{chat_id}")
async def chat_history(user_id: int, chat_id: int):
    try:
        history = await mongo_db_client.retrieve_conversation(user_id, chat_id)
        return {"history": history}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@router.post("/save_message")
async def save_message(conversation_infor: ConversationInfor):
    try:
        await mongo_db_client.insert_or_update_conversation(conversation_infor)
        return {"message": "Message saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

