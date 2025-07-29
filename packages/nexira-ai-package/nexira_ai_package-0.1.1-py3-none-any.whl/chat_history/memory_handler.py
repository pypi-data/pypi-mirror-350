from src.mongo_handler import AsyncBaseMongoDBHandler
from src.chat_history.schema import UserThread, ConversationInfor
from datetime import datetime

class MemoryHandler(AsyncBaseMongoDBHandler):
    def __init__(self, db_name: str, collection_name: str):
        super().__init__(db_name, collection_name)

    async def clear_collection(self):
        """Clear all documents from the collection."""
        await self.delete_many({})
        print(f"Collection '{self.collection_name}' cleared.")

    async def clear_conversation(self, thread_infor: UserThread):
        """Clear a specific conversation."""
        print(thread_infor)
        await self.delete_one(
            {"user_id": thread_infor.user_id, "chat_id": thread_infor.chat_id}
        )

    async def insert_or_update_conversation(self, conversation_infor: ConversationInfor):
        if not conversation_infor.messages:
            print("No messages provided. Skipping update.")
            return

        print(conversation_infor)
        messages_as_dicts = [
            {"role": msg.role, "content": msg.content, "timestamp": msg.timestamp, "message_id": msg.message_id}
            for msg in conversation_infor.messages
        ]

        await self.update_one(
            {
                "user_id": conversation_infor.user_thread.user_id,
                "chat_id": conversation_infor.user_thread.chat_id,
                "agent_name": conversation_infor.user_thread.agent_name
            },
            {
                "$setOnInsert": {
                    "user_id": conversation_infor.user_thread.user_id,
                    "chat_id": conversation_infor.user_thread.chat_id,
                    "agent_name": conversation_infor.user_thread.agent_name,
                    "created_at": datetime.utcnow(),
                },
                "$push": {
                    "messages": {
                        "$each": messages_as_dicts
                    }
                },
            },
            upsert=True,
        )

    async def retrieve_conversation(self, thread_infor: UserThread) -> ConversationInfor:
        conversation = await self.find_one(
            {
                "user_id": thread_infor.user_id,
                "chat_id": thread_infor.chat_id,
                "agent_name": thread_infor.agent_name,
            }
        )
        if conversation:
            conversation["_id"] = str(conversation["_id"])  # Convert ObjectId to string
            return conversation
        print(
            f"No conversation found for user_id '{thread_infor.user_id}' and thread_id '{thread_infor.chat_id}'."
        )
        return {}