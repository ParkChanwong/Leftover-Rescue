from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.client.llm_client import FakeLlmClient, OpenAiLlmClient
from app.core.config import get_settings
from app.core.exception import register_exception_handler
from app.router import ingredient_router, recipe_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    settings = get_settings()

    if settings.fake_llm or settings.openai_api_key is None:
        print(f"[lifespan] 가짜 LLM 클라이언트를 사용한다 (FAKE_LLM={settings.fake_llm}, 키 있음={settings.openai_api_key is not None})")
        app.state.llm_client = FakeLlmClient(settings)
    else:
        print(f"[lifespan] OpenAI 클라이언트를 사용한다 (model={settings.openai_model})")
        app.state.llm_client = OpenAiLlmClient(settings)

    yield

    await app.state.llm_client.close()

app = FastAPI(title="Leftover Rescue", version="0.1.0", lifespan=lifespan)

register_exception_handler(app)

app.include_router(ingredient_router.router)
app.include_router(recipe_router.router)
