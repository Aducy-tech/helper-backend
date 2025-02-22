from pydantic import BaseModel, Field
from src.enums.ai_models import Model


class AIRequest(BaseModel):
    text: str
    model: Model = Field(
        description="AI model to use for generation",
        default=Model.GPT_4O_MINI  # Other models are being developed
    )


class AIResponse(BaseModel):
    text: str
    tokens: int


class MinimumTokensForAIResponse(BaseModel):
    tokens: int


class ComposeEssayRequest(BaseModel):
    theme: str = Field(
        json_schema_extra={"example": "Трагизм Мцыри"},
        description="Тема сочинения"
    )
    author: str = Field(
        json_schema_extra={"example": "Н. Ю. Лермонтов"},
        description="Автор сочинения"
    )
    word_count: int = Field(
        json_schema_extra={"example": 250},
        description="Количество слов в сочинении"
    )

    additional_info: str | None = Field(
        json_schema_extra={"example": "Трагический герой"},
        description="Дополнительная информация"
    )


class ComposeEssayResponse(AIResponse):
    pass


class MinimumTokensForComposeEssayResponse(BaseModel):
    tokens: int
