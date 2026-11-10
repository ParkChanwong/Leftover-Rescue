from fastapi import APIRouter

from app.dependencies import RecipeServiceDep
from app.schema.recipe import RecipeResponse

router = APIRouter(prefix="/api/recipes", tags=["레시피"])

@router.post("/recommend", summary="등록된 재료로 레시피 추천")
async def recommend_recipes(service: RecipeServiceDep) -> RecipeResponse:
    return await service.recommend()
