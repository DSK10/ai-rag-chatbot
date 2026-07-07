from fastapi import APIRouter
from app.services.db import check_db
from app.services.ollama_client import check_ollama

router = APIRouter()

@router.get("/health")
async def health():
    return {"db": await check_db(), "ollama": await check_ollama()}

@router.get("/health/db")
async def health_db():
    return {"db_connected": await check_db()}