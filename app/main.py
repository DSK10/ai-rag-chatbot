from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.routers import chat, health

from app.services.db import get_pool, close_pool
from app.services.ollama_client import close_ollama_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    await get_pool()
    yield
    await close_pool()
    await close_ollama_client()


app = FastAPI(
    title="AI RAG Chatbot",
    description="A chatbot that uses AI and RAG to answer questions",
)

app.include_router(chat.router)
app.include_router(health.router)
