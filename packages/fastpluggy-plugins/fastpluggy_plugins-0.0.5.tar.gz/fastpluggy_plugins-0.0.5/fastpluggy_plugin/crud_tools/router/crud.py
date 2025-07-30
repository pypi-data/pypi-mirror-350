import logging
from typing import Type

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy import select
from sqlalchemy.orm import Session

from fastpluggy.core.database import get_db
from fastpluggy.core.dependency import get_view_builder, get_fastpluggy
from fastpluggy.core.flash import FlashMessage
from fastpluggy.core.models_tools.sqlalchemy import ModelToolsSQLAlchemy
from fastpluggy.core.tools.fastapi import redirect_to_previous
from fastpluggy.core.view_builer.components.form import FormView
from fastpluggy.core.view_builer.components.list import ListButtonView
from fastpluggy.core.view_builer.components.model import ModelView
from fastpluggy.core.view_builer.components.raw import RawView
from fastpluggy.core.view_builer.components.table_model import TableModelView
from fastpluggy.fastpluggy import FastPluggy
from ..crud_admin import CrudAdmin
from ..schema import CrudAction

crud_view_router = APIRouter(prefix='/action', tags=["front_action"])


def get_admin_instance(model_name: str, default_crud_class:bool=True):
    try:
        model_class = ModelToolsSQLAlchemy.get_model_class(model_name)

        registry = FastPluggy.get_global("crud_admin_registry")
        if registry is not None:
            admin = registry.get_admin(model_class.__name__)
            if admin:
                return admin

        if default_crud_class:
            return CrudAdmin(model=model_class)
        return None

    except Exception as e:
        logging.exception(e)
        return None


@crud_view_router.api_route("/{model_name}/list", methods=["GET", "POST"], name="crud_list")
async def list_item(model_name: str, request: Request, view_builder=Depends(get_view_builder),
                    fast_pluggy=Depends(get_fastpluggy)):
    admin = get_admin_instance(model_name)

    # 3) gather inline‑and‑page actions from the admin
    inline_actions = admin.get_inline_actions(CrudAction.LIST)
    page_action = admin.get_actions(CrudAction.LIST)
    field_list = admin.configure_fields(context=CrudAction.LIST)

    items = []
    if page_action:
        items.append(ListButtonView(
            buttons=page_action
        ))

    show_item = TableModelView(
        model=admin.model,
        exclude_fields=admin.get_excluded_fields(context=CrudAction.LIST),
        field_callbacks=admin.get_fields_callbacks(context=CrudAction.LIST),
        filters=admin.get_list_filters(context=CrudAction.LIST),
        default_sort=admin.get_default_sort(),
        fields=field_list.keys(),
        links=inline_actions
    )
    items.append(show_item)

    return view_builder.generate(
        request,
        title=admin.get_page_title(CrudAction.LIST),
        items=items,
    )


@crud_view_router.api_route("/{model_name}/view/{item_id}", methods=["GET", "POST"], name="crud_view")
async def view_item(item_id: int, model_name: str, request: Request, db: Session = Depends(get_db),
                    view_builder=Depends(get_view_builder)):

    admin = get_admin_instance(model_name)
    model_class = admin.model
    stmt = select(model_class).where(getattr(model_class, admin.primary_key_field) == item_id)
    instance = db.execute(stmt).scalar_one_or_none()

    show_item = ModelView(
        model=admin.model,
        filters={admin.primary_key_field: item_id},
        field_callbacks=admin.get_fields_callbacks(context=CrudAction.VIEW),
    )

    return view_builder.generate(
        request,
        title=admin.get_page_title(CrudAction.VIEW, item=instance),
        items=[show_item]
    )


@crud_view_router.api_route("/{model_name}/create", methods=["GET", "POST"], name="crud_new")
async def create_item(model_name: str, request: Request, db: Session = Depends(get_db),
                      view_builder=Depends(get_view_builder), fast_pluggy=Depends(get_fastpluggy)):

    model_class = ModelToolsSQLAlchemy.get_model_class(model_name)
    if model_class is None:
        FlashMessage.add(request=request, message=f"Model {model_name} not found !")
        return view_builder.generate(request, title=f"Create {model_name}", items=[])

    admin = get_admin_instance(model_class.__name__)

    # Get custom field configurations from the admin
    configured_fields = admin.configure_fields(CrudAction.CREATE)

    # Process the configured fields to separate regular fields from form panels
    custom_fields = {}
    form_panels = []

    for name, field in configured_fields.items():
        if hasattr(field, 'type') and field.type == 'panel':
            form_panels.append(field)
        else:
            # Call the field to get the actual WTForms field
            custom_fields[name] = field() if callable(field) else field
    items = []

    form_view = FormView(
        model=model_class,
        submit_label=admin.get_submit_label(CrudAction.CREATE),
        exclude_fields=admin.get_excluded_fields(CrudAction.CREATE),
        fields=custom_fields,
        # TODO: Add support for form panels when FormView supports it
    )
    items.append(form_view)

    dependency_scripts = admin.get_js_scripts(context=CrudAction.EDIT)
    if dependency_scripts:
        raw_view = RawView(
            source="\n".join(dependency_scripts)
        )
        items.append(raw_view)

    if request.method == "POST":
        form_data = await request.form()
        form = form_view.get_form(form_data)
        if form.validate():
            instance = model_class()
            form.populate_obj(instance)

            db.add(instance)
            db.commit()
            FlashMessage.add(request, f"{model_name} created successfully!", "success")
            return redirect_to_previous(request)

    return view_builder.generate(
        request,
        title=admin.get_page_title(CrudAction.CREATE),
        items=items
    )


@crud_view_router.api_route("/{model_name}/edit/{item_id}", methods=["GET", "POST"], name="crud_edit")
async def edit_item(item_id: int, model_name: str, request: Request, db: Session = Depends(get_db),
                    view_builder=Depends(get_view_builder), fast_pluggy=Depends(get_fastpluggy)):
    model_class = ModelToolsSQLAlchemy.get_model_class(model_name)

    admin = get_admin_instance(model_class.__name__)
    stmt = select(model_class).where(getattr(model_class, admin.primary_key_field) == item_id)
    instance = db.execute(stmt).scalar_one_or_none()

    if not instance:
        FlashMessage.add(request, f"{model_name} {item_id} not found!", "error")
        return redirect_to_previous(request)

    # Get custom field configurations from the admin
    configured_fields = admin.configure_fields(CrudAction.EDIT)

    # Process the configured fields to separate regular fields from form panels
    custom_fields = {}
    form_panels = []

    for name, field in configured_fields.items():
        if hasattr(field, 'type') and field.type == 'panel':
            form_panels.append(field)
        else:
            # Call the field to get the actual WTForms field
            custom_fields[name] = field() if callable(field) else field

    items = []
    form_view = FormView(
        model=model_class,
        data=instance,
        submit_label=admin.get_submit_label(CrudAction.EDIT),
        exclude_fields=admin.get_excluded_fields(CrudAction.EDIT),
        additional_fields=custom_fields,
        # TODO: Add support for form panels when FormView supports it
    )
    items.append(form_view)

    dependency_scripts = admin.get_js_scripts(context=CrudAction.EDIT)
    if dependency_scripts:
        raw_view = RawView(
            source="\n".join(dependency_scripts)
        )
        items.append(raw_view)

    if request.method == "POST":
        form_data = await request.form()
        form = form_view.get_form(form_data)
        if form.validate():
            form.populate_obj(instance)
            db.commit()
            FlashMessage.add(request, f"{model_name} updated successfully!", "success")
            return redirect_to_previous(request)

    return view_builder.generate(
        request,
        title=admin.get_page_title(CrudAction.EDIT, item=instance),
        items=items
    )


@crud_view_router.get("/{model_name}/delete/{item_id}", response_class=RedirectResponse, name="crud_delete")
async def delete_item(item_id: int, model_name: str, request: Request, db: Session = Depends(get_db)):
    model_class = ModelToolsSQLAlchemy.get_model_class(model_name)

    admin = get_admin_instance(model_class.__name__)
    stmt = select(model_class).where(getattr(model_class, admin.primary_key_field) == item_id)

    instance = db.execute(stmt).scalar_one_or_none()
    if not instance:
        FlashMessage.add(request, f"{model_name} {item_id} not found!", "error")
    else:
        db.delete(instance)
        db.commit()
        FlashMessage.add(request, f"{model_name} deleted successfully!", "success")

    return redirect_to_previous(request)
