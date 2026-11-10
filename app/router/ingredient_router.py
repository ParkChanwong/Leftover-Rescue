from fastapi import APIRouter

from app.dependencies import IngredientServiceDep
from app.schema.ingredient import IngredientCreateRequest, IngredientResponse, IngredientUpdateRequest

router = APIRouter(prefix="/api/ingredients", tags=["재료"])

@router.get("", summary="재료 조회 (keyword를 비우면 전체 조회)")
def find_ingredients(service: IngredientServiceDep, keyword: str | None = None) -> list[IngredientResponse]:
    return service.find_ingredients(keyword)

@router.get("/{ingredient_id}", summary="재료 하나 조회")
def find_ingredient(ingredient_id: int, service: IngredientServiceDep) -> IngredientResponse:
    return service.find_ingredient(ingredient_id)

@router.post("", status_code=201, summary="재료 추가 (같은 이름이 있으면 409)")
def register_ingredient(request: IngredientCreateRequest, service: IngredientServiceDep) -> IngredientResponse:
    return service.register_ingredient(request)

@router.put("/{ingredient_id}", summary="재료 수정 (이름과 수량을 통째로 바꿈)")
def update_ingredient(
    ingredient_id: int, request: IngredientUpdateRequest, service: IngredientServiceDep
) -> IngredientResponse:
    return service.update_ingredient(ingredient_id, request)

@router.delete("/{ingredient_id}", status_code=204, summary="재료 삭제")
def delete_ingredient(ingredient_id: int, service: IngredientServiceDep) -> None:
    service.delete_ingredient(ingredient_id)
