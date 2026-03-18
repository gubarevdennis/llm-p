from pydantic import BaseModel, Field
from typing import Optional

class ChatRequest(BaseModel):
    prompt: str = Field(..., min_length=1)
    system: Optional[str] = None
    max_history: int = Field(default=5, ge=0, le=20)
    temperature: float = Field(default=0.7, ge=0.0, le=2.0)

class ChatResponse(BaseModel):
    answer: str