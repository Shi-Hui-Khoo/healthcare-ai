from pydantic import BaseModel
from typing import Any, Mapping, List

class Request(BaseModel):
    history: List[Mapping[str, Any]] = None

class Response(BaseModel):
    response: str = None