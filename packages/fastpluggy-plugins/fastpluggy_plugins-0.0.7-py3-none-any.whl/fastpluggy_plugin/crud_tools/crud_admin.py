from typing import List, Union, Dict, Any, Type

from wtforms import Field

from fastpluggy.core.models_tools.sqlalchemy import ModelToolsSQLAlchemy
from .crud_link_helper import CrudLinkHelper
from .field_types import FieldType, IdFieldType, TextFieldType, TextareaFieldType, IntegerFieldType, BooleanFieldType
from .field_types.date_fields import DateTimeFieldType
from .field_types.enum_fields import EnumFieldType
from .field_types.timedelta_fields import TimedeltaFieldType
from .schema import CrudAction
from fastpluggy.core.models_tools.shared import ModelToolsShared


class CrudAdmin:
    # Override in subclasses: either a single PK name or a list of PK names
    pk: Union[str, List[str]] = None

    # Subclasses must set this to their SQLAlchemy model class
    model = None  # type: ignore

    default_excluded_fields = ["created_at", "updated_at"]

    def __init__(self, model: Type[Any] = None):
        self.model = model or self.model
        if self.model is None:
            raise ValueError(f"{self.__class__.__name__}.model must be set as a class attribute")

    @property
    def primary_key_field(self) -> str:
        """
        Returns primary key field names for this model,
        using either the override in `self.pk` or reflecting the model.
        """
        if self.pk is not None:
            return self.pk

        pks = ModelToolsSQLAlchemy.get_model_primary_keys(self.model)
        # pks = self.primary_key_fields
        if len(pks) != 1:
            raise ValueError(
                f"Model {self.model.__name__} has multiple primary keys {pks}. "
                "Override `pk` to a single field or handle composite keys."
            )
        return pks[0]

    def get_excluded_fields(self, context: CrudAction) -> List[str]:
        if context == CrudAction.CREATE or context == CrudAction.LIST:
            return self.default_excluded_fields
        if context == CrudAction.EDIT:
            return self.default_excluded_fields
        return []

    def get_submit_label(self, context: CrudAction) -> str:
        return f"{context.title()} {self.model.__name__}"

    def get_page_title(self, context: CrudAction, item=None) -> str:
        """
        Generate a dynamic page title. Override in subclasses for custom titles.
        """
        if context in (CrudAction.EDIT, CrudAction.VIEW) and item is not None:
            pk_val = getattr(item, self.primary_key_field, '')
            return f"{context.title()} {self.model.__name__} {pk_val}"
        return f"{context.title()} {self.model.__name__}"

    def on_create(self, instance, db):
        ...

    def on_update(self, instance, db):
        ...

    def on_delete(self, instance, db):
        ...

    def configure_filters(self, filters):
        """
        Override in subclasses to add Filters to the List view.
        """
        return filters

    def get_list_filters(self, context: CrudAction) -> dict:
        """
        To filter the query on table view / sqlalchemy select
        """
        return {}

    def get_inline_actions(self, context: CrudAction) -> List[dict]:
        """
        Override to return row-level CRUD action links.
        """
        return [
            CrudLinkHelper.get_crud_link(
                self.model,
                CrudAction.VIEW,
                label="View",
                css_class="btn btn-sm btn-info",
            ),
        ]

    def get_actions(self, context: CrudAction) -> List[dict]:
        """
        Override to return page-level CRUD action links.
        """
        if context == CrudAction.LIST:
            return [
                CrudLinkHelper.get_crud_link(
                    self.model,
                    CrudAction.CREATE,
                    css_class="btn btn-success",
                )
            ]
        return []

    def configure_fields(self, context: CrudAction) -> Dict[str, Field]:
        """
        Override in subclasses to configure custom field types and properties.

        This method allows you to customize the form fields used in CRUD operations.
        You can specify field types, validators, and other properties.

        Example:
            def configure_fields(self, context: CrudAction) -> Dict[str, Field]:
                title = StringField('Title', validators=[DataRequired()])
                description = TextAreaField('Description')
                price = DecimalField('Price', places=2)

                if context == CrudAction.CREATE:
                    return {'title': title, 'description': description, 'price': price}
                elif context == CrudAction.EDIT:
                    return {'title': title, 'description': description}
                return {}

        Args:
            context: The CRUD action context (CREATE, EDIT, LIST, VIEW)

        Returns:
            A dictionary mapping field names to WTForms Field objects
        """

        fields_metadata = ModelToolsShared.get_model_metadata(
            model=self.model,
        )
        field_types: Dict[str, FieldType] = {}

        for name, meta in fields_metadata.items():
            ftype = meta.get('type')
            enum_cls = meta.get('enum_class')
            required = meta.get('required', False)
            default = meta.get('default', None)
            help_text = meta.get('description')
            primary_key = meta.get('primary_key', False)
            readonly = meta.get('readonly', False)

            # Determine the correct FieldType class
            if primary_key or name == 'id':
                cls: Type[FieldType] = IdFieldType
            elif enum_cls:
                cls = EnumFieldType
            elif ftype == 'datetime':
                cls = DateTimeFieldType
            elif ftype == 'string':
                cls = TextFieldType
            elif ftype == 'text':
                cls = TextareaFieldType
            elif ftype == 'int':
                cls = IntegerFieldType
            elif ftype == 'bool' or ftype == 'boolean':
                cls = BooleanFieldType
            elif ftype == 'enum':
                cls = EnumFieldType
            elif ftype == 'timedelta':
                cls = TimedeltaFieldType
            # Add more custom mappings as needed
            else:
                # Fallback to generic text input
                cls = TextFieldType

            # Prepare kwargs for instantiation
            kwargs: Dict[str, Any] = {}
            if default is not None:
                kwargs['default'] = default
            if help_text:
                kwargs['help_text'] = help_text
            # Pass enum_class to EnumFieldType
            if cls is EnumFieldType and enum_cls:
                kwargs['enum_class'] = enum_cls

            # Instantiate
            field_types[name] = cls(name, required=required, **kwargs)

        return field_types

    def get_default_sort(self):
        """
        Return the default sort configuration as a dict:
        Example:
            return {"column": "created_at", "order": "desc"}

        Returns:
            A dictionary with 'column' and 'order' keys.
        """
        return None

    def get_js_scripts(self, context: CrudAction):
        configured_fields = self.configure_fields(context=context)
        dependency_scripts = [
            field.render_dependency_js(context=context)
            for field in configured_fields.values()
            if hasattr(field, 'render_dependency_js')
        ]
        return dependency_scripts

    def get_fields_callbacks(self, context: CrudAction):
        configured_fields = self.configure_fields(context=context)

        # now collect each field’s callback script, keyed by the field’s name
        fields_callbacks = {
            name: field.get_field_callback(context=context)
            for name, field in configured_fields.items()
            if hasattr(field, 'get_field_callback')
        }

        return fields_callbacks
