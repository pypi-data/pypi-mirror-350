from pydantic import BaseModel
from pydantic.v1 import BaseSettings


def b64encode_filter(value):
    import base64
    """Filter to convert binary data to base64 string."""
    if value:
        return base64.b64encode(value).decode('utf-8')
    return ''


def pydantic_model_dump(model):
    # seems not used anymore
    if isinstance(model, BaseModel):
        return model.model_dump()
    if isinstance(model, BaseSettings):
        return model.dict()
    raise ValueError("Provided object is not a Pydantic model or settings model.")