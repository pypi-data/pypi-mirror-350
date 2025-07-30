from typing import Optional, List, Any, Callable, Union, Type

from wtforms import SelectField, Field

from ..field_types import FieldType, MixinEntityTools
from ..schema import CrudAction


class DynamicSelectFieldType(FieldType, MixinEntityTools):
    def __init__(
            self,
                 name: str,
                 label: Optional[str] = None,
                 validators: Optional[List[Any]] = None,
                 required: bool = False,
                 help_text: Optional[str] = None,
                 depends_on: Optional[str] = None,
                 query_factory: Optional[Callable[[Any], Any]] = None,
                 get_label: Union[str, Callable] = '__str__',
                 placeholder: str = 'Select an option',

                 model_name: Optional[str] = None,
                 **kwargs):
        super().__init__(name, label, validators, required, help_text, **kwargs)

        self.depends_on = depends_on
        # depends on is used if we need to wait another field to be complete to make query
        self.query_factory = query_factory
        self.get_label = get_label
        self.placeholder = placeholder
        self.model_name = model_name or 'Model'

        self.kwargs['choices'] = [(0, placeholder)]  # populated by JS after user selection
        self.kwargs['validate_choice'] = False

    def get_field_class(self) -> Type[Field]:
        return SelectField

    def render_dependency_js(self, context: CrudAction) -> str:
        if not self.depends_on:
            return ''

        js = f"""
        <script>
        document.addEventListener('DOMContentLoaded', function () {{
            bindDynamicSelect(
                '{self.depends_on}',
                '{self.name}',
                '/plugin/crud_tools/dynamic-select/{self.model_name}/{self.name}?value={{' + '{self.depends_on}' + '}}',
                '{self.placeholder}'
            );
        }});
        </script>
        """
        return js
