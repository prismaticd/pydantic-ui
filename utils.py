from copy import deepcopy


def datetime_schema_field(existing_schema_element: dict) -> dict:
    updated_schema_element = deepcopy(existing_schema_element)
    updated_schema_element.update({"format": "datetime-local"})
    if "options" not in updated_schema_element:
        updated_schema_element["options"] = {}
    options = updated_schema_element["options"]
    options.update({"grid_columns": 4, "flatpickr": {"wrap": True, "time_24hr": True, "allowInput": True}})
    return updated_schema_element
