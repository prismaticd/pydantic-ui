import datetime
import json
import pathlib
from typing import List

from datatables import DataTableModel


class Brewery(DataTableModel):
    id: int
    name: str
    brewery_type: str
    street: str
    city: str
    state: str
    postal_code: str
    country: str
    longitude: float
    latitude: float
    phone: str
    website_url: str
    updated_at: datetime.datetime

    def get_json(self):
        return json.dumps(self.get_dict())

    def get_values(self):
        return self.get_dict().values()

    @classmethod
    def id_field(cls):
        return "id"

    def format_field_for_datatable(self, field):
        value = self.get_field_value(field)
        if field == "id":
            return f"<a href='http://127.0.0.1:8000/{self.__class__.__name__}/{value}'>{value}</a>"
        return value


def get_breweries() -> List[Brewery]:
    p = pathlib.Path("fixtures/breweries.json")
    list_brews = json.loads(p.read_text())
    brew_list = []
    for brew_data in list_brews:
        brew_list.append(Brewery(**brew_data))

    return brew_list


MODEL_CONFIG = {
    'Brewery': {
        'class': Brewery,
        'data': get_breweries()
    }
}

