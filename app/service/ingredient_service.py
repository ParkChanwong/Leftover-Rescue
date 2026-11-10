from app.core.exception import DuplicateIngredientError, IngredientNotFoundError
from app.domain.ingredient import Ingredient
from app.repository.ingredient_repository import IngredientRepository
from app.schema.ingredient import IngredientCreateRequest, IngredientResponse, IngredientUpdateRequest

class IngredientService:
    def __init__(self, repository: IngredientRepository):
        self.repository = repository

    def find_ingredients(self, keyword: str | None) -> list[IngredientResponse]:
        # 키워드가 없거나 공백뿐이면 전체를 조회한다.
        keyword = keyword.strip() if keyword else ""
        ingredients = self.repository.find_by_keyword(keyword) if keyword else self.repository.find_all()
        return [IngredientResponse.from_ingredient(ing) for ing in ingredients]

    def find_ingredient(self, ingredient_id: int) -> IngredientResponse:
        return IngredientResponse.from_ingredient(self._get_or_raise(ingredient_id))

    def register_ingredient(self, request: IngredientCreateRequest) -> IngredientResponse:
        # 같은 이름의 재료가 이미 있으면 추가하지 않는다. 수량을 바꾸려면 수정 API를 쓴다.
        if self.repository.find_by_name(request.name) is not None:
            raise DuplicateIngredientError(request.name)

        saved = self.repository.save(Ingredient(0, request.name, request.quantity or None))
        return IngredientResponse.from_ingredient(saved)

    def update_ingredient(self, ingredient_id: int, request: IngredientUpdateRequest) -> IngredientResponse:
        ingredient = self._get_or_raise(ingredient_id)

        # 이름을 바꿀 때 다른 재료와 이름이 겹치면 막는다. 자기 자신과 같은 이름은 허용한다.
        same_name = self.repository.find_by_name(request.name)
        if same_name is not None and same_name.id != ingredient_id:
            raise DuplicateIngredientError(request.name)

        ingredient.name = request.name
        ingredient.quantity = request.quantity or None
        return IngredientResponse.from_ingredient(self.repository.save(ingredient))

    def delete_ingredient(self, ingredient_id: int) -> None:
        self._get_or_raise(ingredient_id)
        self.repository.delete(ingredient_id)

    def _get_or_raise(self, ingredient_id: int) -> Ingredient:
        ingredient = self.repository.find_by_id(ingredient_id)
        if ingredient is None:
            raise IngredientNotFoundError(ingredient_id)
        return ingredient
