import json
from datetime import datetime

from pydantic import BaseModel

from utils import datetime_schema_field

SCHEMA_TYPE_FUNCTION_MAP = {
    datetime: datetime_schema_field,
}


class DataTableModel(BaseModel):
    @classmethod
    def id_field(cls):
        raise NotImplementedError(f"ID field not implemented in {cls.__name__}")

    @classmethod
    def _datatable_headers(cls):
        return list(cls.__fields__)

    def to_datatable_row(self):
        return [self.format_field_for_datatable(field) for field in self._datatable_headers()]

    def format_field_for_datatable(self, field_name):
        return self.get_field_value(field_name)

    def get_field_value(self, field):
        return getattr(self, field)

    @classmethod
    def to_datatables(cls, object_list: list):
        return {"columns": cls._datatable_headers(), "data": [d.to_datatable_row() for d in object_list]}

    @classmethod
    def autocomplete_fields(cls):
        """Return a string list of all fields that use autocomplete. You must define a function for autocomplete,
        by creating a javascript file
        """
        return set()

    @classmethod
    def all_js_autocomplete_function_paths(cls):
        return [f"/static/js/{cls.__name__}/{field}.js" for field in cls.autocomplete_fields()]

    def to_json_editor_representation(self, **kwargs):
        schema = self.schema()
        autocomplete_fields = self.autocomplete_fields()
        properties = schema["properties"]
        for field, model_field in self.__fields__.items():
            if field in autocomplete_fields:
                properties[field]["format"] = "autocomplete"
                properties[field]["options"] = {"autocomplete": None}
            convert_function = SCHEMA_TYPE_FUNCTION_MAP.get(model_field.type_)
            if convert_function is not None:
                updated_element = convert_function(properties[field])
                properties[field].update(updated_element)
        return json.dumps(schema, indent=2)
