from ollama import AsyncClient, ResponseError
from app.config import settings

_client = AsyncClient(host=settings.ollama_host)

class OllamaUnavailableError(Exception):
    """Raised when ollama model is not reachable"""


async def get_chat_reply(text: str) -> str:
    try:
        result = await _client.chat(
            model=settings.ollama_model,
            messages=[
                {"role": "user", "content": text}
            ]
        )
    except ResponseError as e:
        raise OllamaUnavailableError(f"Response error from ollama {e}") from e
    except Exception as e:
        raise OllamaUnavailableError(f"Unknown exception occured : {e}") from e
    return result.message.content


async def check_ollama() -> bool:
    try:
        await _client.list()
        return True
    except Exception:
        return False

async def close_ollama_client():
    close = getattr(_client, "aclose", None)
    if close is not None:
        await close()
    else:
        inner = getattr(_client, "_client", None)
        if inner is not None:
            await inner.aclose()