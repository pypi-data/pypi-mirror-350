# codegen: frontend, sdk
from typing import Optional

from pydantic import BaseModel


class Key(BaseModel):
    id: Optional[int] = 0
    date_created: Optional[float] = 0
    key_value: Optional[str] = None
    company_id: int = 0
    description: str = ""
    owner: str = ""
    type: str = ""
    obfuscated: bool = False
    key_map: Optional["KeyIdMap"] = None


class KeyIdMap(BaseModel):
    openai_api_key: Optional[int] = 0
    groq_api_key: Optional[int] = 0
    anthropic_api_key: Optional[int] = 0
    cerebras_api_key: Optional[int] = 0
    azure_api_key: Optional[int] = 0
    sambanova_api_key: Optional[int] = 0
    gemini_api_key: Optional[int] = 0
    deepseek_api_key: Optional[int] = 0


class KeyMap(BaseModel):
    openai_api_key: Optional[Key] = None
    groq_api_key: Optional[Key] = None
    anthropic_api_key: Optional[Key] = None
    cerebras_api_key: Optional[Key] = None
    azure_api_key: Optional[Key] = None
    sambanova_api_key: Optional[Key] = None
    gemini_api_key: Optional[Key] = None
    deepseek_api_key: Optional[Key] = None


Key.model_rebuild()
