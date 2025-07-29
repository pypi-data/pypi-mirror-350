from typing import Optional, Any

from pydantic import BaseModel


class RedisKey(BaseModel):
    key: str
    type: str
    ttl: int
    size: Optional[int] = None
    preview: Optional[Any] = None
    value: Any = None
