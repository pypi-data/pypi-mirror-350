from wtforms import Field, DateTimeLocalField
from wtforms.widgets import Input
from datetime import datetime
from typing import Optional, List, Any, Type

from ..field_types import FieldType


class MonthInput(Input):
    """Custom input widget for HTML5 month picker."""
    input_type = 'month'

    validation_attrs = {}


class MonthFieldWT(Field):
    """WTForms field for <input type="month">."""

    widget = MonthInput()

    def _value(self):
        if self.data:
            # Return as YYYY-MM format for the input
            return self.data.strftime('%Y-%m')
        return ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = datetime.strptime(valuelist[0], '%Y-%m')
            except ValueError:
                self.data = None
                raise ValueError('Not a valid month format (expected YYYY-MM).')


class MonthFieldType(FieldType):
    """Your MonthField abstraction based on your FieldType system."""

    def __init__(self,
                 name: str,
                 label: Optional[str] = None,
                 validators: Optional[List[Any]] = None,
                 required: bool = False,
                 help_text: Optional[str] = None,
                 **kwargs):
        super().__init__(name, label, validators, required, help_text, **kwargs)

    def get_field_class(self) -> Type[Field]:
        return MonthFieldWT


class DateTimeFieldType(FieldType):
    """DateTime field."""

    def __init__(self, name: str, label: Optional[str] = None, validators: Optional[List[Any]] = None,
                 required: bool = False, help_text: Optional[str] = None, render_as_choice: bool = False, **kwargs):
        """
        Initialize a datetime field.

        Args:
            render_as_choice: Whether to render as dropdown selects instead of a datetime picker
        """
        super().__init__(name, label, validators, required, help_text, **kwargs)
        self.render_as_choice = render_as_choice

    def get_field_class(self) -> Type[Field]:
        return DateTimeLocalField
