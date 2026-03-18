# app/services/openrouter_client.py
import httpx
import json

from app.core.config import settings
from app.core.errors import ExternalServiceError

class OpenRouterClient:
    def __init__(self):
        self.base_url = settings.OPENROUTER_BASE_URL
        self.model = settings.OPENROUTER_MODEL
        
        self.headers = {
            "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
            "HTTP-Referer": settings.OPENROUTER_SITE_URL,
            "X-Title": settings.OPENROUTER_APP_NAME,
            "Content-Type": "application/json",
        }

    async def ask(self, messages: list[dict], temperature: float) -> str:
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature
        }
        
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.post(
                    f"{self.base_url}/chat/completions", 
                    headers=self.headers, 
                    json=payload,
                    timeout=30.0 # Таймаут для ответа LLM
                )
                
                resp.raise_for_status() # Вызовет исключение для 4xx/5xx кодов
                
                data = resp.json()
                # Предполагаем стандартную структуру ответа OpenAI-совместимых API
                return data["choices"][0]["message"]["content"]

        except httpx.HTTPStatusError as e:
            # Ловим ошибки HTTP, возвращаемые OpenRouter
            try:
                error_detail = e.response.json().get('error', {}).get('message', str(e.response.text))
            except json.JSONDecodeError:
                error_detail = str(e.response.text)
                
            raise ExternalServiceError(
                detail=f"OpenRouter API Error ({e.response.status_code}): {error_detail}"
            )
            
        except httpx.RequestError as e:
            # Ловим сетевые ошибки (нет соединения, таймаут и т.д.)
            raise ExternalServiceError(
                detail=f"Network or connection error during OpenRouter request: {e}"
            )