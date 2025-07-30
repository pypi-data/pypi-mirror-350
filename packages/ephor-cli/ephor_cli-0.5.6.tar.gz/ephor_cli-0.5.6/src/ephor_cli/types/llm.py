from enum import Enum
from pydantic import BaseModel


class LLMProvider(Enum):
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AWS = "aws"


class Model(BaseModel):
    name: str
    provider: LLMProvider
