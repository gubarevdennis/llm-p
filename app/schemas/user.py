from pydantic import BaseModel, ConfigDict
from datetime import datetime

class UserPublic(BaseModel):
    id: int
    email: str
    role: str
    created_at: datetime

    # Разрешает Pydantic читать данные из атрибутов ORM-модели
    model_config = ConfigDict(from_attributes=True)