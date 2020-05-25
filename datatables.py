import json
from datetime import datetime

from pydantic import BaseModel

from utils import datetime_schema_field

SCHEMA_TYPE_FUNCTION_MAP = {
    datetime: datetime_schema_field,
}


class DataTableModel:
    @classmethod
    def id_field(cls):
        raise NotImplementedError(f"ID field not implemented in {cls.__name__}")

    @classmethod
    def _datatable_headers(cls):
        return list(cls.kind.__fields__)

    @classmethod
    def to_datatable_row(cls, object):
        return [cls.format_field_for_datatable(object, field) for field in cls._datatable_headers()]

    @classmethod
    def format_field_for_datatable(cls, object, field_name):
        value = getattr(object, field_name)
        if field_name == cls.id_field():
            return f"<a href='http://127.0.0.1:8000/{cls.__name__}/{value}'>{value}</a>"
        return value

    @classmethod
    def to_datatables(cls, object_list: list):
        return {"columns": cls._datatable_headers(), "data": [cls.to_datatable_row(d) for d in object_list]}

    @classmethod
    def autocomplete_fields(cls):
        """Return a string list of all fields that use autocomplete. You must define a function for autocomplete,
        by creating a javascript file
        """
        return set()

    @classmethod
    def all_js_autocomplete_function_paths(cls):
        return [f"/static/js/{cls.__name__}/{field}.js" for field in cls.autocomplete_fields()]

    @classmethod
    def to_json_editor_representation(cls, object, **kwargs):
        schema = object.schema()
        autocomplete_fields = cls.autocomplete_fields()
        properties = schema["properties"]
        for field, model_field in object.__fields__.items():
            if field in autocomplete_fields:
                properties[field]["format"] = "autocomplete"
                properties[field]["options"] = {"autocomplete": None}
            convert_function = SCHEMA_TYPE_FUNCTION_MAP.get(model_field.type_)
            if convert_function is not None:
                updated_element = convert_function(properties[field])
                properties[field].update(updated_element)
        return json.dumps(schema, indent=2)
