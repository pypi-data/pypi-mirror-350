import os
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters, CommandHandler
import httpx
from datetime import datetime
import requests

class NexiraBot:
    def __init__(self, bot_token: str, api_url: str, mongodb_url: str = ''):
        self.api_url = api_url
        self.mongodb_url = mongodb_url
        self.application = ApplicationBuilder().token(bot_token).build()
        self.application.add_handler(CommandHandler("start", self.start))
        self.application.add_handler(CommandHandler("new_chat", self.new_chat))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("🤖 Hello! I'm your LLM chatbot. Send me a message!")

    async def new_chat(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        print(update)
        if self.mongodb_url:
            requests.post(self.mongodb_url + "/chat/clear_chat", json={
                "user_id": update.effective_user.id,
                "chat_id": update.effective_chat.id,
                "agent_name": ""
            })
        await update.message.reply_text("🤖 New chat started!")

    async def store_message_mongodb(self, client: httpx.AsyncClient, user_id: int, chat_id: int, bot_name: str, messages: list):
        if self.mongodb_url:
            await client.post(self.mongodb_url + "/chat/save_message", json={
                "user_thread": {
                    "user_id": user_id,
                    "chat_id": chat_id,
                    "agent_name": bot_name
                },
                "messages": messages
            })
        
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        messages = []
        text = update.effective_message.text
        user_id = str(update.effective_user.id)
        chat_id = str(update.effective_chat.id)
        is_bot = update.effective_user.is_bot
        message_id = update.effective_message.message_id
        timestamp = update.effective_message.date
        messages.append({"role": "user" if not is_bot else "assistant", "content": text, "timestamp": timestamp.isoformat(), "message_id": message_id})

        try:
            url = self.api_url + "/llm_model/ask"
            async with httpx.AsyncClient(timeout=10.0) as client:
                #await self.store_message_mongodb(client, text, user_id, chat_id, is_bot, message_id, timestamp)
                response = await client.post(url, json={'question': text})
                message_obj = await update.message.reply_text(response.json()['response'])
                bot_text = message_obj.text
                bot_id = str(message_obj.from_user.id)
                bot_name = message_obj.from_user.first_name
                chat_id = str(message_obj.chat.id)
                is_bot = message_obj.from_user.is_bot
                message_id = message_obj.message_id
                timestamp = message_obj.date
                messages.append({"role": "assistant" if is_bot else "user", "content": bot_text, "timestamp": timestamp.isoformat(), "message_id": message_id})
                await self.store_message_mongodb(client, user_id, chat_id, bot_name, messages)
        except Exception as e:
            await update.message.reply_text(f"Error: {str(e)}")
    
    def run(self):
        print("🤖 Bot is running...")
        self.application.run_polling()
