# crud_link_helper.py

from fastpluggy.core.models_tools.sqlalchemy import ModelToolsSQLAlchemy
from .schema import CrudAction
from .template_tools import url_for_crud


class CrudLinkHelper:

    @staticmethod
    def link_has_label(link, label):
        """
        Check if a link (dict or object) has the specified label.
        """
        if isinstance(link, dict):
            return link.get("label") == label
        elif hasattr(link, "label"):
            return getattr(link, "label") == label
        return False

    @staticmethod
    def get_crud_link(
        model,
        action: str | CrudAction,
        label: str = None,
        css_class: str = None,
    ) -> dict:
        """
        Generate a CRUD link for the given model and action.

        :param model: The model class to generate the link for.
        :param action: The CRUD action ('view', 'create', 'edit', 'delete').
        :param label: Customize the label of the link.
        :param css_class: Optional CSS class to apply. If not provided, a sensible default is used per action.
        :return: A dictionary representing the link.
        """

        # If given a SQLAlchemy model class, use its name
        if ModelToolsSQLAlchemy.is_sqlalchemy(model):
            model = model.__name__

        action = CrudAction.from_any(action)

        # sensible defaults per action
        chosen_class = css_class or action.default_css_class

        if action == CrudAction.VIEW:
            return {
                "url": url_for_crud(model_name=model, action=CrudAction.VIEW, entity_id="<id>"),
                "column": "id",
                "label": label or "View",
                "css_class": chosen_class,
            }

        if action == CrudAction.CREATE:
            return {
                "url": url_for_crud(model_name=model, action=CrudAction.CREATE),
                "label": label or "Create",
                "css_class": chosen_class,
            }

        if action == CrudAction.EDIT:
            return {
                "url": url_for_crud(model_name=model, action=CrudAction.EDIT, entity_id="<id>"),
                "column": "id",
                "label": label or "Edit",
                "css_class": chosen_class,
            }

        if action == CrudAction.DELETE:
            return {
                "url": url_for_crud(model_name=model, action=CrudAction.DELETE, entity_id="<id>"),
                "column": "id",
                "label": label or "Delete",
                "css_class": chosen_class,
                "onclick": "return confirm('Are you sure?');",
            }

        if action == CrudAction.LIST:
            return {
                "url": url_for_crud(model_name=model, action=CrudAction.LIST),
                "label": label or "List",
                "css_class": chosen_class,
            }

        # if we reach here, action was unrecognized
        supported = ", ".join(a.value for a in CrudAction)
        raise ValueError(f"Invalid action '{action}'. Supported actions: {supported}.")
