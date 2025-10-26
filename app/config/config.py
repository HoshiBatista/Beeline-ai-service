from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """!
    @brief Основной класс конфигурации, агрегирующий все настройки проекта.
    """
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        extra='ignore',
        case_sensitive=False
    )

    OPENROUTER_API_KEY: str = Field(..., description="API ключ от OpenRouter.ai.")
    OPENROUTER_BASE_URL: str = Field(default="https://openrouter.ai/api/v1", description="Базовый URL для OpenRouter API.")
    OPENROUTER_MODEL: str = Field(default="anthropic/claude-3-haiku-20240307", description="ID модели на OpenRouter (Claude 3 Haiku).")
    
    DEFAULT_MAX_NEW_TOKENS: int = Field(default=512, description="Макс. кол-во токенов в ответе.")
    
    APP_HOST: str = Field(default="0.0.0.0", description="IP-адрес для запуска сервиса.")
    APP_PORT: int = Field(default=8000, description="Порт веб-сервиса.")
    LOG_LEVEL: Literal["debug", "info", "warning", "error"] = Field(default="info", description="Уровень логирования.")


settings = Settings()