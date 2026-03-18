# app/usecases/chat.py

from app.repositories.chat_messages import ChatRepository
from app.services.openrouter_client import OpenRouterClient
from app.schemas.chat import ChatRequest

class ChatUseCase:
    def __init__(self, 
                 message_repo: ChatRepository, 
                 client: OpenRouterClient):
        self.repo = message_repo
        self.client = client

    async def ask(self, user_id: int, data: ChatRequest) -> str:
        
        # 1. Сборка контекста и сохранение запроса пользователя
        
        # 1a. Получаем историю (максимум data.max_history сообщений)
        history_orm = await self.repo.get_history(user_id, data.max_history)
        
        # 1b. Формируем список сообщений для LLM
        messages_for_llm = []
        
        # Добавляем системное сообщение, если оно есть
        if data.system:
            messages_for_llm.append({"role": "system", "content": data.system})
            
        # Добавляем историю
        for msg in history_orm:
            messages_for_llm.append({"role": msg.role, "content": msg.content})
            
        # Добавляем текущий пользовательский запрос
        messages_for_llm.append({"role": "user", "content": data.prompt})
        
        # 1c. Сохраняем запрос пользователя в БД
        await self.repo.add_message(user_id, "user", data.prompt)
        
        # 2. Запрос к LLM
        
        answer_content = await self.client.ask(
            messages=messages_for_llm,
            temperature=data.temperature
        )
        
        # 3. Сохранение ответа ассистента
        await self.repo.add_message(user_id, "assistant", answer_content)
        
        # 4. Возврат текста ответа
        return answer_content