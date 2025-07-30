import enum
from typing import Type, Optional, List, Any

from wtforms import Field, SelectField

from ..field_types import FieldType

from ..schema import CrudAction


class EnumFieldType(FieldType):
    """Field for selecting an Enum value."""

    ## Would you also want an auto-converter
    # (for example, auto-cast the submitted string back into an enum on form.validate_on_submit())? 👉 That would make it even smoother!
    ##I can add it if you want. 🚀

    def __init__(self,
                 name: str,
                 enum_class: Type[enum.Enum],
                 label: Optional[str] = None,
                 validators: Optional[List[Any]] = None,
                 required: bool = False,
                 help_text: Optional[str] = None,
                 get_choice_label: Optional[str] = None,
                 **kwargs):
        """
        Initialize an Enum field.

        Args:
            enum_class: The Enum class to use for choices
        """
        super().__init__(name, label, validators, required, help_text, **kwargs)
        self.enum_class = enum_class

        self.get_choice_label = lambda e: (
            getattr(e, get_choice_label, e.name.replace("_", " ").title())
            if get_choice_label else e.name.replace("_", " ").title()
        )

        self.kwargs['choices'] = [
            (e.value, self.get_choice_label(e))
            for e in enum_class
        ]
        #self.kwargs['choices'] = [(e.value, e.name.replace("_", " ").title()) for e in enum_class]

    def get_field_class(self) -> Type[Field]:
        return SelectField

    def get_field_callback(self, context: CrudAction):
         return self.get_choice_label