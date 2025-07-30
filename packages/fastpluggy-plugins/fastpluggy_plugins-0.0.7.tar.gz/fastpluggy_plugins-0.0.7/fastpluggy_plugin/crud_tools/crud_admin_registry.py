import logging
from typing import Type
from .crud_admin import CrudAdmin

class CrudAdminRegistry:
    def __init__(self):
        self._registry: dict[str, CrudAdmin] = {}

    def register(self, admin_class: Type[CrudAdmin]):
        """
        Register an admin by its class. The admin_class must have a `model` attribute set.
        """
        model_class = getattr(admin_class, 'model', None)
        if model_class is None:
            raise ValueError(f"{admin_class.__name__}.model must be set as a class attribute")

        logging.info(f"Registering {model_class.__name__} with {admin_class.__name__}")
        # Instantiate without parameters; admin_class.model is used internally
        instance = admin_class()
        self._registry[model_class.__name__] = instance

    def get_admin(self, model_name: str) -> CrudAdmin:
        return self._registry.get(model_name)

    def to_dict(self) -> dict[str, str]:
        return {
            model_name: admin.__class__.__name__
            for model_name, admin in self._registry.items()
        }
