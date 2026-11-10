# Leftover Rescue

냉장고에 남은 재료를 등록해 두고, 등록한 재료로 LLM에게 레시피를 추천받는 FastAPI 서버입니다.

DB 없이 서버 메모리에 재료를 저장합니다. 서버를 다시 켜면 초기 재료 7개로 돌아갑니다.

## 기술 스택

- Python 3.14
- FastAPI, Pydantic, pydantic-settings
- OpenAI Responses API (비동기 클라이언트)
- uv (패키지 관리)

## 시작하기

### 1. 의존성 설치

```bash
uv sync
```

### 2. 환경 변수 설정

`.env.example`을 복사해 `.env`를 만들고 값을 채웁니다. `.env`는 Git에 올라가지 않습니다.

```bash
cp .env.example .env
```

| 변수                       | 기본값       | 설명                                                        |
| -------------------------- | ------------ | ----------------------------------------------------------- |
| `OPENAI_API_KEY`           | 없음         | OpenAI API 키. 없으면 가짜 LLM으로 동작합니다.              |
| `OPENAI_MODEL`             | `gpt-6-luna` | 사용할 모델                                                 |
| `OPENAI_REASONING_EFFORT`  | `none`       | `none`, `minimal`, `low`, `medium`, `high`, `xhigh` 중 하나 |
| `OPENAI_MAX_OUTPUT_TOKENS` | `2000`       | 최대 출력 토큰. 너무 작으면 레시피가 중간에 잘립니다.       |
| `OPENAI_TIMEOUT_SECONDS`   | `30`         | OpenAI 응답 제한 시간(초)                                   |
| `FAKE_LLM`                 | `false`      | `true`면 키가 있어도 가짜 LLM을 사용합니다.                 |
| `FAKE_LLM_DELAY_SECONDS`   | `1`          | 가짜 LLM이 응답하기 전에 기다리는 시간(초)                  |

`.env.example`의 값은 자리 표시용입니다. 그대로 두면 설정 검증에 실패해 서버가 켜지지 않으니, 위 표의 형식에 맞는 값으로 바꿔 주세요.

### 3. 서버 실행

```bash
uv run fastapi dev
```

실행한 뒤 http://127.0.0.1:8000/docs 에서 Swagger로 API를 확인할 수 있습니다.

비용 없이 테스트하려면 가짜 LLM으로 실행합니다.

```bash
FAKE_LLM=true uv run fastapi dev
```

## API

| 메서드   | 경로                               | 설명                                    |
| -------- | ---------------------------------- | --------------------------------------- |
| `GET`    | `/api/ingredients?keyword=`        | 재료 검색. `keyword`를 비우면 전체 조회 |
| `GET`    | `/api/ingredients/{ingredient_id}` | 재료 하나 조회                          |
| `POST`   | `/api/ingredients`                 | 재료 추가. 같은 이름이 있으면 409       |
| `PUT`    | `/api/ingredients/{ingredient_id}` | 재료 수정. 이름과 수량을 통째로 바꿈    |
| `DELETE` | `/api/ingredients/{ingredient_id}` | 재료 삭제                               |
| `POST`   | `/api/recipes/recommend`           | 등록된 재료로 레시피 추천               |

### 재료 추가 / 수정

```json
{
  "name": "대파",
  "quantity": "3개"
}
```

| 필드       | 필수 | 규칙                                                                                                            |
| ---------- | ---- | --------------------------------------------------------------------------------------------------------------- |
| `name`     | O    | 1~50자. 앞뒤 공백은 지워집니다.                                                                                 |
| `quantity` | X    | 최대 20자. 단위까지 함께 적습니다 (예: `300g`, `1.5L`, `3개`, `반 단`). 양념처럼 수량이 의미 없으면 생략합니다. |

응답:

```json
{
  "id": 8,
  "name": "대파",
  "quantity": "3개"
}
```

### 재료 규칙

- **이름 중복:** 같은 재료인지 확인할 때 공백을 모두 지우고 영어는 소문자로 바꿔 비교합니다. `파마산 치즈`가 있으면 `파마산치즈`, `Olive Oil`이 있으면 `olive oil`도 409로 막힙니다. 저장되는 이름은 입력한 표기 그대로입니다.
- **수량 변경:** 같은 재료를 다시 추가하지 않고 `PUT`으로 수정합니다. `PUT`은 통째로 바꾸는 방식이라 `quantity`를 생략하면 수량이 비워집니다.
- **검색:** 이름 중복과 같은 규칙으로 비교하며, 이름의 일부만 맞아도 찾습니다. `파마산치즈`로 검색해도 `파마산 치즈`가 나옵니다.

### 레시피 추천

등록된 전체 재료를 LLM에 보내 레시피 3개를 추천받습니다.

- 레시피마다 요리 이름, 사용할 재료와 분량, 조리 순서, 추가로 필요한 재료를 알려 줍니다.
- 수량이 적혀 있지 않은 재료는 충분히 있다고 가정합니다.
- 등록된 재료가 없으면 LLM을 호출하지 않고 400을 돌려줍니다.

응답:

```json
{
  "answer": "## 1. 알리오 올리오\n**사용 재료**\n- 스파게티면 100g\n...",
  "model": "gpt-6-luna"
}
```

가짜 LLM은 레시피를 만들지 않고, LLM에 보냈을 재료 목록을 그대로 돌려줍니다. 이때 `model`은 `fake-llm`입니다.

## 에러 응답

```json
{
  "code": "ERROR_CODE_00003",
  "description": "중복된 재료",
  "detail": "이미 등록된 재료입니다. name=대파"
}
```

| 상태 코드 | `code`              | 상황                                                             |
| --------- | ------------------- | ---------------------------------------------------------------- |
| 404       | `ERROR_CODE_00001`  | 없는 재료를 조회, 수정, 삭제                                     |
| 400       | `ERROR_CODE_00002`  | 재료가 하나도 없는데 레시피 추천 요청                            |
| 409       | `ERROR_CODE_00003`  | 이미 있는 이름으로 추가하거나 수정                               |
| 502       | `ERROR_CODE_00011`  | OpenAI 호출 실패 (키 오류, 요청 한도 초과, 시간 초과, 연결 실패) |
| 422       | (FastAPI 기본 형식) | 요청 값 검증 실패 (이름 누락, 길이 초과 등)                      |

## 프로젝트 구조

```
app/
├── main.py                 # 앱 생성, 라우터·예외 처리 등록, LLM 클라이언트 준비
├── dependencies.py         # 저장소·서비스·LLM 클라이언트 의존성 주입
├── core/
│   ├── config.py           # .env 설정
│   └── exception.py        # 예외와 에러 응답
├── domain/
│   └── ingredient.py       # 재료 도메인
├── schema/
│   ├── base.py             # camelCase 변환 공통 모델
│   ├── ingredient.py       # 재료 요청·응답
│   └── recipe.py           # 레시피 응답
├── repository/
│   └── ingredient_repository.py  # 메모리(dict) 기반 재료 저장소
├── service/
│   ├── ingredient_service.py     # 재료 조회·추가·수정·삭제
│   └── recipe_service.py         # 레시피 추천 (프롬프트 구성)
├── client/
│   └── llm_client.py       # OpenAI 클라이언트와 가짜 LLM 클라이언트
└── router/
    ├── ingredient_router.py
    └── recipe_router.py
```

## 참고

- 재료는 메모리에 저장되므로 서버를 다시 켜면 아래 초기 재료로 돌아갑니다.
  스파게티면 100g, 올리브유 200ml, 마늘 10개, 소금, 페페론치노 12개, 파슬리, 파마산 치즈
- 사용자 구분이 없어서 모든 요청이 하나의 냉장고를 함께 씁니다.
