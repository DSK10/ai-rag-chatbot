from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID


# pydantic model for chat request and response


class ChatRequest(BaseModel):
    text: str = Field(..., min_length=2, max_length=4000)
    message_id: Optional[UUID] = None


class ChatResponse(BaseModel):
    reply: str
    message_id: UUID
