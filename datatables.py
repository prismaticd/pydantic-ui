import json
from datetime import datetime

from pydantic import BaseModel


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

    def to_json_editor_representation(self, **kwargs):
        schema = self.schema()
        properties = schema["properties"]
        for field, model_field in self.__fields__.items():
            # todo: example, refactor
            if model_field.type_ == datetime:
                properties[field]["format"] = "datetime-local"
                properties[field]["options"] = {
                    "grid_columns": 4,
                    "flatpickr": {"wrap": True, "time_24hr": True, "allowInput": True},
                }
        return json.dumps(schema, indent=kwargs.get("indent", None))
