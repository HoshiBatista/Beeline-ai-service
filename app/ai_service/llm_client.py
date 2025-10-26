from openai import OpenAI
from app.config.config import settings

client = OpenAI(
    api_key=settings.OPENROUTER_API_KEY,
    base_url=settings.OPENROUTER_BASE_URL,
)

def generate_text(prompt: str, temperature: float) -> str:
    """!
    @brief Выполняет генерацию текста через OpenAI-совместимый API OpenRouter.
    """
    try:
        chat_completion = client.chat.completions.create(
            model=settings.OPENROUTER_MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=max(temperature, 0.01),
            max_tokens=settings.DEFAULT_MAX_NEW_TOKENS,
        )
        response_text = chat_completion.choices[0].message.content
        return response_text.strip()
    
    except Exception as e:
        raise ConnectionError(f"Ошибка при обращении к OpenRouter API: {e}")