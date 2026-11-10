from dataclasses import dataclass

@dataclass
class Ingredient:
    # 재료 번호(PK)
    id: int
    # 재료 명
    name: str
    # 재료 수량
    quantity: str | None = None
