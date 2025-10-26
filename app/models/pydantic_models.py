from pydantic import BaseModel, Field
from typing import List, Dict, Any, Literal

class UserData(BaseModel):
    """! @brief Модель данных клиента с поддержкой произвольных полей."""
    user_id: str
    profile: Dict[str, Any] = Field(default_factory=dict)
    activity: Dict[str, Any] = Field(default_factory=dict)
    communication_history: List[Dict[str, Any]] = Field(default_factory=list)

class ProductData(BaseModel):
    """! @brief Модель данных о продукте."""
    product_name: str
    description: str
    key_benefits: List[str]
    target_audience_keywords: List[str] = Field(default_factory=list)

class GenerationRequest(BaseModel):
    """! @brief Модель входящего запроса на генерацию."""
    user_data: UserData
    product_data: ProductData
    message_type: Literal['push', 'чат', 'email']
    tone: Literal['дружелюбный', 'официальный', 'нейтральный', 'продающий', 'заботливый'] = 'нейтральный'
    num_variants: int = Field(default=1, ge=1, le=3)
    creativity_level: float = Field(default=0.7, ge=0.1, le=1.0)

class GenerationResponse(BaseModel):
    """! @brief Модель ответа сервиса."""
    status: str
    generated_variants: List[str]