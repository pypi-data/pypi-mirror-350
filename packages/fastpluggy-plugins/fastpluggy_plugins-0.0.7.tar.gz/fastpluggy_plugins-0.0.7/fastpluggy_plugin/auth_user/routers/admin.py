from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.responses import HTMLResponse, RedirectResponse
from wtforms import PasswordField
from wtforms.validators import DataRequired, Length

from auth_user.auth.basic_auth import BasicAuthManager
from fastpluggy.core.database import get_db
from fastpluggy.core.menu.decorator import menu_entry
from fastpluggy.core.dependency import get_view_builder, get_fastpluggy
from fastpluggy.core.flash import FlashMessage
from fastpluggy.core.view_builer.components.form import FormView
from fastpluggy.core.view_builer.components.list import ListButtonView
from fastpluggy.core.view_builer.components.render_field_tools import RenderFieldTools
from fastpluggy.core.view_builer.components.table_model import TableModelView

# Define a constant for the common prefix
ADMIN_USERS_PREFIX = "/admin/users"

user_router = APIRouter(
    prefix=ADMIN_USERS_PREFIX,
    tags=["admin"]
)

@menu_entry(label="List Users", type='admin')
@user_router.get("/", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db),
               fast_pluggy = Depends(get_fastpluggy),
               view_builder=Depends(get_view_builder)):
    user_model = fast_pluggy.auth_manager.user_model
    items = [
        ListButtonView(
            buttons=[
                {
                    "url": f"{ADMIN_USERS_PREFIX}/add",
                    "label": "Add New User",
                },
            ]
        ),
        TableModelView(
            model=user_model,
            field_callbacks={
                user_model.is_admin: RenderFieldTools.render_boolean
            },
            exclude_fields=[user_model.hashed_password],
        )]
    return view_builder.generate(
        request,
        title="Users",
        items=items
    )


@user_router.api_route("/add", methods=["GET", "POST"])
async def add_user(
        request: Request,
        db: Session = Depends(get_db),
        fast_pluggy=Depends(get_fastpluggy),
        view_builder=Depends(get_view_builder),
):
    user_model = fast_pluggy.auth_manager.user_model

    form_view = FormView(
        model=user_model,
        exclude_fields=['hashed_password', user_model.created_at, user_model.updated_at],
        readonly_fields=["id"],
        additional_fields={
            'password': PasswordField('Password', validators=[DataRequired(), Length(min=6)]),
        },
        submit_label="Create User",
    )

    if request.method == "POST":
        form_data = await request.form()
        form = form_view.get_form(form_data)
        if form.validate():
            # Create a new user instance
            user = user_model()
            form.populate_obj(user)

            # Handle password separately
            if form.password.data:
                user.hashed_password = BasicAuthManager.hash_password(form.password.data)
            else:
                FlashMessage.add(request, "Password is required", "error")
                return RedirectResponse(f"{ADMIN_USERS_PREFIX}/add", status_code=303)

            user.id = None
            db.add(user)
            db.commit()
            FlashMessage.add(request, f"User '{user.username}' created successfully!", "success")
            return RedirectResponse(ADMIN_USERS_PREFIX, status_code=303)
        else:
            # Handle form errors
            FlashMessage.add(request, "Form is invalid. Please correct the errors and try again.", "error")

    # Render the form (either with errors or as a blank form)
    return view_builder.generate(
        request,
        title="Add User",
        items=[form_view]
    )


@user_router.api_route("/edit/{user_id}", methods=["GET", "POST"])
async def edit_user(
        user_id: int,
        request: Request,
        db: Session = Depends(get_db),
        fast_pluggy=Depends(get_fastpluggy),
        view_builder=Depends(get_view_builder),
):
    user_model = fast_pluggy.auth_manager.user_model

    user = db.query(user_model).filter(user_model.id == user_id).first()
    if not user:
        FlashMessage.add(request, f"User {user_id} not found !", "error")
        return RedirectResponse(ADMIN_USERS_PREFIX, status_code=303)

    form_view = FormView(
        model=user_model,
        exclude_fields=['hashed_password', user_model.created_at, user_model.updated_at],
        readonly_fields=["id"],
        additional_fields={
            'password': PasswordField('Password')
        },
        data=user,
        submit_label="Update User",
    )

    if request.method == "POST":
        form_data = await request.form()
        form = form_view.get_form(form_data)
        if form.validate():
            form.populate_obj(user)

            # Handle password separately
            if form.password.data:
                user.hashed_password = pwd_context.hash(form.password.data)

            db.commit()
            FlashMessage.add(request, f"User '{user.username}' updated successfully!", "success")
            return RedirectResponse(ADMIN_USERS_PREFIX, status_code=303)

    # Render the form (either with errors or as a blank form)
    return view_builder.generate(
        request,
        title="Edit User",
        items=[form_view]
    )

