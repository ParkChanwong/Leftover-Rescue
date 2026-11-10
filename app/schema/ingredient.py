from pydantic import ConfigDict, Field

from app.schema.base import CamelModel
from app.domain.ingredient import Ingredient

class IngredientCreateRequest(CamelModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=50, description="재료 이름", examples=["대파"])
    quantity: str | None = Field(
        default=None,
        max_length=20,
        description="수량. 단위까지 함께 적는다 (예: 300g, 1.5L, 3개, 반 단). 양념처럼 수량이 의미 없으면 생략한다.",
        examples=["3개"]
    )

# 수정은 추가와 같은 필드를 받아 통째로 바꾼다. quantity를 생략하면 수량이 비워진다.
class IngredientUpdateRequest(IngredientCreateRequest):
    pass

class IngredientResponse(CamelModel):
    id: int
    name: str
    quantity: str | None

    @classmethod
    def from_ingredient(cls, ingredient: Ingredient) -> IngredientResponse:
        return cls(
            id=ingredient.id,
            name=ingredient.name,
            quantity=ingredient.quantity
        )
