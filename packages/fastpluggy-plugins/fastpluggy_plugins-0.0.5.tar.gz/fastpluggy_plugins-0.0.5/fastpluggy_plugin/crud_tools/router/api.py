from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

from fastpluggy.core.database import get_db
from fastpluggy.core.models_tools.sqlalchemy import ModelToolsSQLAlchemy
from .crud import get_admin_instance
from ..field_types.dynamic_fields import DynamicSelectFieldType
from ..field_types import MixinEntityTools
from ..schema import CrudAction

crud_api_router = APIRouter()

@crud_api_router.get("/dynamic-select/{model_name}/{field_name}")
async def dynamic_select_endpoint(
    model_name: str,
    field_name: str,
    value: str,
    request: Request,
    db: Session = Depends(get_db)
):
    model_class = ModelToolsSQLAlchemy.get_model_class(model_name)
    if model_class is None:
        return JSONResponse(status_code=404, content={"error": "Field not found"})

    admin = get_admin_instance(model_class.__name__)
    configured_fields = admin.configure_fields(CrudAction.CREATE)

    # Lookup the form field in a global registry
    field: DynamicSelectFieldType = configured_fields.get(field_name)

    if not field or not isinstance(field, DynamicSelectFieldType):
        return JSONResponse(status_code=404, content={"error": "Field not found"})

    # Execute the query factory with the value
    query = field.query_factory(value)
    results = db.execute(query)
    records = results.scalars().all()

    get_value = MixinEntityTools.get_label_for_object(field)

    return [{"id": obj.id, "name": get_value(obj)} for obj in records]
