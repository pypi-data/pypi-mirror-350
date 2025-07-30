class MixinEntityTools:
    @staticmethod
    def get_label_for_object(field):
        if isinstance(field.get_label, str):
            def get_value(obj):
                attr = getattr(obj, field.get_label, None)
                return attr() if callable(attr) else attr
            return get_value
        else:
            get_value = field.get_label
        return get_value
