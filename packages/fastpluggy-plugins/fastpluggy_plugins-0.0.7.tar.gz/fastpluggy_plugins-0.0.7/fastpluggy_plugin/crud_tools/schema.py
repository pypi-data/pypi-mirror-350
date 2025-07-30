# schema.py
from enum import Enum
from typing import Union

class CrudAction(str, Enum):
    LIST   = "list"
    VIEW   = "view"
    CREATE = "create"
    EDIT   = "edit"
    DELETE = "delete"

    @staticmethod
    def action_map() -> dict["CrudAction", str]:
        return {
            CrudAction.LIST:   'crud_list',
            CrudAction.VIEW:   'crud_view',
            CrudAction.CREATE: 'crud_new',
            CrudAction.EDIT:   'crud_edit',
            CrudAction.DELETE: 'crud_delete',
        }

    def to_route_name(self) -> str:
        # Mapping of actions to the route keys.
        return self.action_map().get(self, f"crud_{self.value}")

    @staticmethod
    def from_any(value: Union[str, "CrudAction"]) -> "CrudAction":
        if isinstance(value, CrudAction):
            return value
        if isinstance(value, str):
            try:
                return CrudAction(value.lower())
            except ValueError:
                valid = ", ".join(a.value for a in CrudAction)
                raise ValueError(
                    f"Invalid CRUD action '{value}'. Must be one of: {valid}"
                )
        raise TypeError(f"Unsupported type for CRUD action: {type(value)}")

    @property
    def default_css_class(self) -> str:
        """
        Return the default CSS class for this CRUD action.
        """
        defaults = {
            CrudAction.VIEW:   "btn btn-info",
            CrudAction.CREATE: "btn btn-info",
            CrudAction.EDIT:   "btn btn-info",
            CrudAction.DELETE: "btn btn-danger",
        }
        # LIST has no default button, so return empty string
        return defaults.get(self, "")
