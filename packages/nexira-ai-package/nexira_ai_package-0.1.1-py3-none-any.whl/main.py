from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from chat_history.routes import router as chat_history_router, lifespan

app = FastAPI(
    title="Telegram BotAPI",
    description="API for telegram bot application",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

app.include_router(chat_history_router)


@app.get("/")
async def root():
    return {"message": "Welcome to Mini Mavia API"}


@app.post("/health")
async def health_check():
    return {"status": "healthy"}



if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)

