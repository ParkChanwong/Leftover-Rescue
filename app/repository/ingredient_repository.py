from app.domain.ingredient import Ingredient

# 재료 리스트
def init_ingredient() -> list[Ingredient]:
    return [
        Ingredient(0, "스파게티면", "100g"),
        Ingredient(0, "올리브유", "200ml"),
        Ingredient(0, "마늘", "10개"),
        Ingredient(0, "소금"),
        Ingredient(0, "페페론치노", "12개"),
        Ingredient(0, "파슬리"),
        Ingredient(0, "파마산 치즈"),
    ]

# 이름 비교용 값. 공백을 모두 지우고 영어는 소문자로 바꾼다. 예: "Parmesan 치즈" → "parmesan치즈"
# 저장되는 이름은 바꾸지 않고, 중복 확인과 키워드 검색에서 비교할 때만 쓴다.
def normalize_name(name: str) -> str:
    return "".join(name.split()).lower()

class IngredientRepository:
    def __init__(self):
        self._ingredients: dict[int, Ingredient] = {}
        self._next_id = 1

        for ingredient in init_ingredient():
            self.save(ingredient)

    def find_all(self) -> list[Ingredient]:
        return list(self._ingredients.values())

    def find_by_keyword(self, keyword: str) -> list[Ingredient]:
        target = normalize_name(keyword)
        return [ing for ing in self._ingredients.values() if target in normalize_name(ing.name)]

    def find_by_id(self, ingredient_id: int) -> Ingredient | None:
        return self._ingredients.get(ingredient_id)

    def find_by_name(self, name: str) -> Ingredient | None:
        target = normalize_name(name)
        return next((ing for ing in self._ingredients.values() if normalize_name(ing.name) == target), None)

    def save(self, ing: Ingredient) -> Ingredient:
        if ing.id == 0:
            ing.id = self._next_id
            self._next_id += 1

        self._ingredients[ing.id] = ing
        return ing

    def delete(self, ingredient_id: int) -> None:
        self._ingredients.pop(ingredient_id, None)
