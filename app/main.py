import uvicorn
import asyncio
from fastapi import FastAPI, HTTPException
from app.models.pydantic_models import GenerationRequest, GenerationResponse
from app.ai_service.promt_builder import create_prompt
from app.ai_service.llm_client import generate_text
from app.config.config import settings

app = FastAPI(
    title="Beeline AI Service (OpenRouter + Claude)",
    version="0.0.1",
    description="Сервис персонализации сообщений на базе Claude 3."
)

@app.post("/generate", response_model=GenerationResponse)
async def generate_messages_endpoint(request: GenerationRequest):
    """! @brief Эндпоинт для генерации сообщений."""
    try:
        prompt = create_prompt(request)
        tasks = [
            asyncio.to_thread(generate_text, prompt, request.creativity_level)
            for _ in range(request.num_variants)
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        successful_variants = []
        for res in results:
            if isinstance(res, Exception): raise res
            successful_variants.append(res)

        return GenerationResponse(status="success", generated_variants=successful_variants)
    except ConnectionError as e:
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host=settings.APP_HOST,
        port=settings.APP_PORT,
        log_level=settings.LOG_LEVEL,
        reload=True
    )