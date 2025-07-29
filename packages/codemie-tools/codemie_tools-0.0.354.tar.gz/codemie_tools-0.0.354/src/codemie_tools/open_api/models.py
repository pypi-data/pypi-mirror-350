from pydantic import BaseModel
from typing import Optional


class OpenApiConfig(BaseModel):
    spec: str
    is_basic_auth: bool = False
    username: Optional[str] = None
    api_key: str
    timeout: int = 60
