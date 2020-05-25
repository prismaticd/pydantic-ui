from typing import List, Set

from models import Beer, Brewery, get_beers, get_breweries
from pydantic_ui.datatables import DataTableModel
from pydantic_ui.models import UIModel, PydanticUI


class BeerUI(UIModel, DataTableModel):
    kind = Beer

    @classmethod
    def id_field(cls) -> str:
        return "id"

    @classmethod
    def get_all_data(cls) -> List[Beer]:
        return get_beers()


class BreweryUI(UIModel, DataTableModel):
    kind = Brewery

    @classmethod
    def id_field(cls) -> str:
        return "id"

    @classmethod
    def get_all_data(cls) -> List[Brewery]:
        return get_breweries()

    @classmethod
    def autocomplete_fields(cls) -> Set[str]:
        return {"related_wikipedia_title"}


PYDANTIC_UI = PydanticUI()
