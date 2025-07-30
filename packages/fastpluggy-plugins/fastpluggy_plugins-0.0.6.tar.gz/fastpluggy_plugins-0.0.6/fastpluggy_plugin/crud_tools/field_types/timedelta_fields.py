# crud_tools/field_types/timedelta_fields.py

from wtforms import Field
from datetime import timedelta
from ..field_types import FieldType
from ..schema import CrudAction


class TimedeltaInput:
    """
    Render two Bootstrap input-groups: one for weeks, one for days,
    each with a − button, a number input, and a + button.
    """
    def __call__(self, field, **kwargs):
        # already‐computed values (either from POST or initial data)
        weeks = getattr(field, "_weeks", 0)
        days  = getattr(field, "_days", 0)
        name = field.name
        id_  = field.id

        html = f'''
<div class="row timedelta-field">
  <div class="form-group col">
    <div class="input-group">
    <label for="{id_}_weeks" class="input-group-text">Weeks</label>
      <div class="input-group-prepend">
        <button class="btn btn-outline-secondary" type="button"
                onclick="decrement('{name}_weeks')">−</button>
      </div>
      <input type="number"
             class="form-control text-center"
             name="{name}_weeks"
             id="{id_}_weeks"
             value="{weeks}"
             min="0">
      <div class="input-group-append">
        <button class="btn btn-outline-secondary" type="button"
                onclick="increment('{name}_weeks')">+</button>
      </div>
    </div>
  </div>

  <div class="form-group col">
    <div class="input-group">
    <label for="{id_}_days" class="input-group-text">Days</label>
      <div class="input-group-prepend">
        <button class="btn btn-outline-secondary" type="button"
                onclick="decrement('{name}_days')">−</button>
      </div>
      <input type="number"
             class="form-control text-center"
             name="{name}_days"
             id="{id_}_days"
             value="{days}"
             min="0">
      <div class="input-group-append">
        <button class="btn btn-outline-secondary" type="button"
                onclick="increment('{name}_days')">+</button>
      </div>
    </div>
  </div>
</div>
'''
        return html


class TimedeltaField(Field):
    """
    A WTForms Field that reads two sub-inputs (`_weeks`, `_days`)
    and stores a single datetime.timedelta in `.data`.
    """
    widget = TimedeltaInput()

    def __init__(self, label=None, validators=None, default=timedelta(0), **kwargs):
        super().__init__(label=label, validators=validators, default=default, **kwargs)

    def process(self, formdata, data=None, **kwarg):
        # On GET: formdata is empty, data==model value or default
        if data is None:
            data = self.default

        # if POST, read the two sub-fields
        if formdata and formdata.get(f"{self.name}_weeks") is not None:
            try:
                w = int(formdata[f"{self.name}_weeks"])
            except:
                w = 0
            try:
                d = int(formdata[f"{self.name}_days"])
            except:
                d = 0

            self.data = timedelta(weeks=w, days=d)
            self._weeks = w
            self._days  = d
        else:
            # initial GET: split the existing timedelta
            if isinstance(data, timedelta):
                total_days = data.days
                w = total_days // 7
                d = total_days % 7
            else:
                w = d = 0

            self.data = timedelta(weeks=w, days=d)
            self._weeks = w
            self._days  = d

    def _value(self):
        return ""  # not used


class TimedeltaFieldType(FieldType):
    """
    FieldType wrapper so you can do:

        delay = TimedeltaFieldType(
            "delay",
            label="Delay",
            default=timedelta(weeks=2),
        )
    """
    def __init__(self, name, label=None, validators=None, required=False,
                 help_text=None, default=timedelta(0), **kwargs):
        super().__init__(name, label, validators, required, help_text, **kwargs)
        self.kwargs["default"] = default

    def render_dependency_js(self, context: CrudAction) -> str:
        js = f"""
        <script>
          function increment(fieldName) {{
            var el = document.getElementsByName(fieldName)[0];
            el.value = (parseInt(el.value||0) + 1);
          }}
          function decrement(fieldName) {{
            var el = document.getElementsByName(fieldName)[0];
            var v = parseInt(el.value||0);
            el.value = (v > 0 ? v - 1 : 0);
          }}
        </script>
        """
        return js

    def get_field_class(self):
        return TimedeltaField
