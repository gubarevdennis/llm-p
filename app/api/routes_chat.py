from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user_id, handle_errors
from app.repositories.chat_messages import ChatRepository
from app.services.openrouter_client import OpenRouterClient
from app.usecases.chat import ChatUseCase
from app.schemas.chat import ChatRequest, ChatResponse

router = APIRouter(prefix="/chat", tags=["Chat"])

def get_chat_usecase(db: AsyncSession = Depends(get_db)):
    return ChatUseCase(ChatRepository(db), OpenRouterClient())

@router.post("/", response_model=ChatResponse)
async def ask(data: ChatRequest, user_id: int = Depends(get_current_user_id), uc: ChatUseCase = Depends(get_chat_usecase)):
    answer = await handle_errors(uc.ask(user_id, data))
    return ChatResponse(answer=answer)

@router.delete("/history")
async def clear_history(user_id: int = Depends(get_current_user_id), db: AsyncSession = Depends(get_db)):
    repo = ChatRepository(db)
    await repo.clear_history(user_id)
    return {"message": "History cleared"}

@router.get("/history", response_model=list[dict])
async def get_history(
    user_id: int = Depends(get_current_user_id), 
    db: AsyncSession = Depends(get_db)
):
    repo = ChatRepository(db)
    # Используем историю 
    history = await repo.get_history(user_id, max_count=20)
    
    # Преобразуем ORM-объекты в список словарей
    return [
        {"role": msg.role, "content": msg.content, "created_at": msg.created_at} 
        for msg in history
    ]