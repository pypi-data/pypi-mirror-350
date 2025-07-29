from typing import Optional

from .template_tools import url_for_crud
from fastpluggy.core.menu.schema import MenuItem
from .schema import CrudAction


class MenuItemCrud(MenuItem):
    def __init__(
            self,
            model,
            action: str|CrudAction,
            label: str,
            icon: Optional[str] = None,
            entity_id=None,
            entity_id_key: str = "item_id",
            **kwargs  # Additional parameters such as parent_name, permission, position
    ):
        """
        Create a CRUD menu item whose URL is generated using the url_for_crud function.

        Args:
            model: The model class or a string representing the model name.
            action (str): The CRUD action. Supported actions include:
                          "LIST", "VIEW", "CREATE", "EDIT", "DELETE".
            label (str): The display label for the menu item.
            icon (Optional[str]): An optional icon string.
            entity_id: The ID for actions that require an entity.
            entity_id_key (str): The key used in the URL for the entity ID (default is "item_id").
            **kwargs: Additional keyword arguments passed to the base MenuItem.
        """
        # Determine the model name.
        if isinstance(model, type):
            model_name = model.__name__
        else:
            model_name = str(model)

        action = CrudAction.from_any(action)

        # Generate the URL using the url_for_crud function.
        url = url_for_crud(model_name, action, entity_id, entity_id_key)

        # Initialize the base MenuItem with the generated URL and provided attributes.
        super().__init__(label=label, url=url, icon=icon, **kwargs)
