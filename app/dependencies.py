from typing import Annotated

from fastapi import Depends, Request

from app.client.llm_client import LlmClient
from app.repository.ingredient_repository import IngredientRepository
from app.service.ingredient_service import IngredientService
from app.service.recipe_service import RecipeService

ingredient_repository = IngredientRepository()

def get_ingredient_repository() -> IngredientRepository:
    return ingredient_repository

def get_ingredient_service(
    repository: Annotated[IngredientRepository, Depends(get_ingredient_repository)]
) -> IngredientService:
    return IngredientService(repository)

IngredientServiceDep = Annotated[IngredientService, Depends(get_ingredient_service)]

def get_llm_client(request: Request) -> LlmClient:
    return request.app.state.llm_client

def get_recipe_service(
    repository: Annotated[IngredientRepository, Depends(get_ingredient_repository)],
    llm_client: Annotated[LlmClient, Depends(get_llm_client)]
) -> RecipeService:
    return RecipeService(repository, llm_client)

RecipeServiceDep = Annotated[RecipeService, Depends(get_recipe_service)]
