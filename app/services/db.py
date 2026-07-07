import asyncpg
from app.config import settings
from uuid import UUID

_pool : asyncpg.Pool | None = None

async def get_pool() -> asyncpg.Pool:
    global _pool
    if _pool is None:
        _pool = await asyncpg.create_pool(settings.database_url)
    return _pool

async def close_pool():
    global _pool
    if _pool:
        await _pool.close()
        _pool = None

async def check_db() -> bool:
    pool = await get_pool()
    async with pool.acquire() as conn:
        return await conn.fetchval("SELECT 1") == 1

async def save_message(message_id: UUID, input_text: str, output_text: str) -> None:
    pool = await get_pool()
    async with pool.acquire() as conn:
        await conn.execute(
            "INSERT INTO messages (message_id, input, output) VALUES ($1, $2, $3)",
            message_id, input_text, output_text,
        )