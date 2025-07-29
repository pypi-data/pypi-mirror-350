from typing import Callable, Union
from typing import Type, Optional, List, Any

from wtforms import Field
from wtforms import SelectField
from wtforms import StringField, TextAreaField, IntegerField, BooleanField, DecimalField, \
    FileField
from wtforms.validators import DataRequired, NumberRange, Email

from ..field_types.entity_fields import MixinEntityTools
from ..schema import CrudAction
from fastpluggy.core.database import session_scope
from fastpluggy.core.models_tools.sqlalchemy import ModelToolsSQLAlchemy
from fastpluggy.core.view_builer.components.render_field_tools import RenderFieldTools


class FieldType:
    """Base class for field type helpers."""

    def __init__(self, name: str, label: Optional[str] = None, validators: Optional[List[Any]] = None,
                 required: bool = False, help_text: Optional[str] = None, **kwargs):
        """
        Initialize a field type.

        Args:
            name: The field name
            label: The field label (defaults to capitalized name if not provided)
            validators: List of WTForms validators
            required: Whether the field is required
            help_text: Help text to display with the field
            **kwargs: Additional arguments to pass to the WTForms field
        """
        self.model, self.name = ModelToolsSQLAlchemy.split_param(name)
        self.label = label or self.name.replace('_', ' ').capitalize()
        self.validators = validators or []
        self.kwargs = kwargs
        self.help_text = help_text

        if required and not any(isinstance(v, DataRequired) for v in self.validators):
            self.validators.append(DataRequired())

    def __call__(self) -> Field:
        """Create and return the WTForms field."""
        field_class = self.get_field_class()
        field = field_class(
            name=self.name,
            label=self.label,
            validators=self.validators,
            description=self.help_text,
            **self.kwargs
        )
        return field

    def get_field_class(self) -> Type[Field]:
        """Get the WTForms field class to use."""
        raise NotImplementedError("Subclasses must implement get_field_class")


# A generic field that can be customized with any field class
class GenericField(FieldType):
    """Generic field that can be customized with any field class."""

    def __init__(self, name: str, field_class: Type[Field], label: Optional[str] = None,
                 validators: Optional[List[Any]] = None, required: bool = False,
                 help_text: Optional[str] = None, **kwargs):
        """
        Initialize a generic field.

        Args:
            field_class: The WTForms field class to use
        """
        super().__init__(name, label, validators, required, help_text, **kwargs)
        self.field_class = field_class

    def get_field_class(self) -> Type[Field]:
        return self.field_class


class TextFieldType(FieldType):
    """Text input field."""

    def get_field_class(self) -> Type[Field]:
        return StringField


class TextareaFieldType(FieldType):
    """Textarea field for longer text."""

    def get_field_class(self) -> Type[Field]:
        return TextAreaField


class IntegerFieldType(FieldType):
    """Integer field."""

    def __init__(self, name: str, label: Optional[str] = None, validators: Optional[List[Any]] = None,
                 required: bool = False, help_text: Optional[str] = None, min_value: Optional[int] = None,
                 max_value: Optional[int] = None, **kwargs):
        """
        Initialize an integer field.

        Args:
            min_value: Minimum allowed value
            max_value: Maximum allowed value
        """
        super().__init__(name, label, validators, required, help_text, **kwargs)

        if min_value is not None or max_value is not None:
            self.validators.append(NumberRange(min=min_value, max=max_value))

    def get_field_class(self) -> Type[Field]:
        return IntegerField


class BooleanFieldType(FieldType):
    """Boolean field (checkbox)."""

    def __init__(self, name: str, label: Optional[str] = None, validators: Optional[List[Any]] = None,
                 required: bool = False, help_text: Optional[str] = None, **kwargs):
        super().__init__(name, label, validators, required, help_text, **kwargs)

    def get_field_class(self) -> Type[Field]:
        return BooleanField

    def get_field_callback(self, context: CrudAction):
         return  RenderFieldTools.render_boolean


class SelectFieldType(FieldType):
    """Select field (dropdown)."""

    def __init__(self, name: str, choices: List[tuple], label: Optional[str] = None,
                 validators: Optional[List[Any]] = None, required: bool = False,
                 help_text: Optional[str] = None, **kwargs):
        """
        Initialize a select field.

        Args:
            choices: List of (value, label) tuples for the dropdown options
        """
        super().__init__(name, label, validators, required, help_text, **kwargs)
        self.kwargs['choices'] = choices

    def get_field_class(self) -> Type[Field]:
        return SelectField


class AssociationFieldType(FieldType):
    """Field for model associations (foreign keys or many-to-many)."""

    def __init__(self,
                 name: str,
                 query_factory: Optional[Callable[[], Any]] = None,
                 label: Optional[str] = None,
                 validators: Optional[List[Any]] = None,
                 required: bool = False,
                 help_text: Optional[str] = None,
                 get_label: Union[str, Callable] = '__str__',
                 allow_blank: bool = False,
                 blank_text: str = 'Select one',
                 multiple: bool = False,
                 **kwargs):
        """
        Initialize an association field.

        Args:
            query_factory: Function returning the query to populate the dropdown.
            get_label: Attribute name or callable to use as the label.
            allow_blank: Whether to allow an empty selection.
            blank_text: Text for the blank option (only if allow_blank=True).
            multiple: If True, renders a multi-select dropdown.
        """
        super().__init__(name, label, validators, required, help_text, **kwargs)
        self.query_factory = query_factory
        self.get_label = get_label
        self.allow_blank = allow_blank
        self.blank_text = blank_text
        self.multiple = multiple

    def __call__(self, *args, **kwargs) -> Field:
        if self.query_factory is None and self.model is not None:
            related_model = ModelToolsSQLAlchemy.make_fk_selects_sa(self.model, self.name)
            self.query_factory = related_model[0]

        if self.query_factory is not None:
            with session_scope() as db:
                data = db.execute(self.query_factory).scalars().all()

                get_value = MixinEntityTools.get_label_for_object(self)

                choices = [(str(obj.id), get_value(obj)) for obj in data]
                self.kwargs['choices'] = choices

        return super().__call__()

    def get_field_class(self) -> Type[Field]:
        return SelectField


class MoneyFieldType(FieldType):
    """Field for monetary values."""

    def __init__(self, name: str, label: Optional[str] = None, validators: Optional[List[Any]] = None,
                 required: bool = False, help_text: Optional[str] = None, currency: str = 'USD',
                 stored_as_cents: bool = False, num_decimals: int = 2, **kwargs):
        """
        Initialize a money field.

        Args:
            currency: The currency code
            stored_as_cents: Whether the value is stored as cents in the database
            num_decimals: Number of decimal places to display
        """
        super().__init__(name, label, validators, required, help_text, **kwargs)
        self.currency = currency
        self.stored_as_cents = stored_as_cents
        self.num_decimals = num_decimals

        # Set the number of decimal places for the field
        self.kwargs['places'] = num_decimals

    def get_field_class(self) -> Type[Field]:
        return DecimalField


class EmailFieldType(FieldType):
    """Email field."""

    def __init__(self, name: str, label: Optional[str] = None, validators: Optional[List[Any]] = None,
                 required: bool = False, help_text: Optional[str] = None, **kwargs):
        """Initialize an email field."""
        super().__init__(name, label, validators, required, help_text, **kwargs)

        # Add email validator if not already present
        if not any(isinstance(v, Email) for v in self.validators):
            self.validators.append(Email())

    def get_field_class(self) -> Type[Field]:
        return StringField


class FileFieldType(FieldType):
    """File upload field."""

    def get_field_class(self) -> Type[Field]:
        return FileField


class IdFieldType(FieldType):
    """ID field (usually read-only)."""

    def __init__(self, name: str = 'id', label: Optional[str] = 'ID', validators: Optional[List[Any]] = None,
                 required: bool = False, help_text: Optional[str] = None, **kwargs):
        """Initialize an ID field."""
        super().__init__(name, label, validators, required, help_text, **kwargs)

        # ID fields are typically read-only
        self.kwargs['render_kw'] = self.kwargs.get('render_kw', {})
        self.kwargs['render_kw']['readonly'] = True

    def get_field_class(self) -> Type[Field]:
        return IntegerField


# Form panel for grouping fields
class FormPanelType:
    """Panel for grouping fields in a form."""
    def __init__(self, title: str, fields: dict[str, FieldType]):
        self.title = title
        self.fields = fields

    def __call__(self) -> dict:
        return {
            'type': 'panel',
            'title': self.title,
            'fields': list(self.fields.keys())
        }


