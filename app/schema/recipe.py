from app.schema.base import CamelModel

class RecipeResponse(CamelModel):
    answer: str
    model: str
