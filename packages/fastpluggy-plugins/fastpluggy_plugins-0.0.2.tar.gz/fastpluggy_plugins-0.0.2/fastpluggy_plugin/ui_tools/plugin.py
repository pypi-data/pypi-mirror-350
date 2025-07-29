from typing import Annotated

from fastpluggy.core.module_base import FastPluggyBaseModule
from fastpluggy.core.tools.inspect_tools import InjectDependency
from fastpluggy.fastpluggy import FastPluggy


class UiToolsModule(FastPluggyBaseModule):
    module_name :str= "ui_tools"
    module_version:str = "0.0.2"

    module_menu_name :str= "UI Tools"
    module_menu_icon :str= "fa fa-tools"
    module_menu_type :str= "no"

    def after_setup_templates(self, fast_pluggy: Annotated[FastPluggy, InjectDependency]):
        from .template_tools import b64encode_filter, pydantic_model_dump
        from .localization import localizedcurrency, localizeddate, nl2br

        fast_pluggy.templates.env.filters['b64encode'] = b64encode_filter
        fast_pluggy.templates.env.filters['pydantic_model_dump'] = pydantic_model_dump

        fast_pluggy.templates.env.filters["localizedcurrency"] = localizedcurrency
        fast_pluggy.templates.env.filters["localizeddate"] = localizeddate
        fast_pluggy.templates.env.filters["nl2br"] = nl2br

        from .html_render import from_json_filter
        fast_pluggy.templates.env.filters["from_json"] = from_json_filter
