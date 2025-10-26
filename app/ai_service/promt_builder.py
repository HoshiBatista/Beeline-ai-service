from app.models.pydantic_models import GenerationRequest


def _format_dict_for_prompt(data: dict, title: str) -> str:
    """!
    @brief Вспомогательная функция для форматирования словарей в текстовый блок.
    @param data Словарь с данными.
    @param title Заголовок для текстового блока.
    @return Отформатированная строка или пустая строка, если словарь пуст.
    """
    if not any(v for v in data.values()): return ""
    items = "\n".join([f"- {key}: {value}" for key, value in data.items() if value])
    return f"### {title}\n{items}\n"

def create_prompt(request: GenerationRequest) -> str:
    """!
    @brief Создает финальный промпт для Claude с использованием XML-тегов.
    @details Claude отлично понимает структурированные данные, что повышает качество ответа.
    """
    user = request.user_data
    product = request.product_data

    profile_str = _format_dict_for_prompt(user.profile, "Профиль клиента")
    activity_str = _format_dict_for_prompt(user.activity, "Активность клиента")
    product_str = _format_dict_for_prompt(product.dict(), "Информация о продукте")
    
    history_summary = ""
    if user.communication_history:
        clicks = sum(1 for h in user.communication_history if h.get('reaction') == 'clicked')
        purchases = sum(1 for h in user.communication_history if h.get('reaction') == 'purchased')
        history_summary = f"<block title=\"История реакций\">\n- Кликов: {clicks}\n- Покупок: {purchases}\n</block>"

    format_requirements = {
        'push': "PUSH: Очень коротко (до 150 симв.), интрига + 1 CTA. Используй emoji.",
        'чат': "ЧАТ: 2-4 предложения, неформально, дружелюбно. Задай вопрос для диалога.",
        'email': "EMAIL: Тема, Приветствие, Выгоды (списком), Призыв к действию, Подпись."
    }

    prompt = f"""Ты — AI-копирайтер компании Билайн, эксперт по персонализированному маркетингу.

<task_briefing>
Твоя задача — проанализировать данные о клиенте и продукте, а затем сгенерировать текст сообщения в соответствии с заданными правилами. Найди самую убедительную связь между потребностями клиента и преимуществами продукта.
</task_briefing>

<data>
{product_str}
{profile_str}
{activity_str}
{history_summary}
</data>

<generation_rules>
- Тип сообщения: {request.message_type}
- Требования к формату: {format_requirements[request.message_type]}
- Тон: {request.tone}
</generation_rules>

<output_instructions>
Твой ответ должен содержать ТОЛЬКО сгенерированный текст сообщения. Никаких предисловий, комментариев или кавычек. Если это email, начни ответ строго с "Тема: ...".
</output_instructions>
"""
    return prompt