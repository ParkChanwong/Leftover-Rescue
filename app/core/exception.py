from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class IngredientNotFoundError(Exception):
    def __init__(self, ingredient_id: int):
        super().__init__(f"해당 재료가 존재하지 않습니다. id={ingredient_id}")
        self.ingredient_id = ingredient_id

class DuplicateIngredientError(Exception):
    def __init__(self, name: str):
        super().__init__(f"이미 등록된 재료입니다. name={name}")
        self.name = name

class EmptyIngredientError(Exception):
    def __init__(self):
        super().__init__("등록된 재료가 없어 레시피를 추천할 수 없습니다.")

class AiRequestError(Exception):
    pass

def register_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(IngredientNotFoundError)
    def handle_ingredient_not_found(request: Request, e: IngredientNotFoundError):
        return JSONResponse(
            status_code=404,
            content={
                "code": "ERROR_CODE_00001",
                "description": "조회 실패",
                "detail": str(e)
            }
        )

    @app.exception_handler(DuplicateIngredientError)
    def handle_duplicate_ingredient(request: Request, e: DuplicateIngredientError):
        return JSONResponse(
            status_code=409,
            content={
                "code": "ERROR_CODE_00003",
                "description": "중복된 재료",
                "detail": str(e)
            }
        )

    @app.exception_handler(EmptyIngredientError)
    def handle_empty_ingredient(request: Request, e: EmptyIngredientError):
        return JSONResponse(
            status_code=400,
            content={
                "code": "ERROR_CODE_00002",
                "description": "추천 불가",
                "detail": str(e)
            }
        )

    @app.exception_handler(AiRequestError)
    def handle_ai_request_error(request: Request, e: AiRequestError):
        return JSONResponse(
            status_code=502,
            content={
                "code": "ERROR_CODE_00011",
                "description": "AI 응답 실패",
                "detail": str(e)
            }
        )
