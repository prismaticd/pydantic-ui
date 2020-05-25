import datetime
import enum
import json
import pathlib
from typing import List, Set

from pydantic import BaseModel

from datatables import DataTableModel


class Unit(enum.Enum):
    celcius = "celsius"
    litres = "litres"
    kilograms = "kilograms"
    grams = "grams"


class Mesure(BaseModel):
    value: int
    unit: Unit


class MashTemp(BaseModel):
    temp: Mesure
    duration: int = None


class Fermentation(BaseModel):
    temp: Mesure


class Method(BaseModel):
    mash_temp: List[MashTemp]
    fermentation: Fermentation
    twist: str = None


class Malt(BaseModel):
    name: str
    amount: Mesure


class Hops(BaseModel):
    name: str
    amount: Mesure
    add: str
    attribute: str


class Ingredients(BaseModel):
    malt: List[Malt]
    hops: List[Hops]
    yeast: str


class Beer(BaseModel):
    id: int
    name: str
    tagline: str
    first_brewed: str
    description: str
    image_url: str
    abv: float
    ibu: int = None
    target_fg: int
    target_og: int
    ebc: int = None
    srm: int = None
    ph: float = None
    attenuation_level: int
    volume: Mesure
    boil_volume: Mesure
    method: Method
    ingredients: Ingredients
    food_pairing: List[str]
    brewers_tips: str
    contributed_by: str


def get_beers() -> List[Beer]:
    p = pathlib.Path("fixtures/beers.json")
    list_beers = json.loads(p.read_text())
    beer_list = []
    for beer in list_beers:
        beer_list.append(Beer(**beer))

    return beer_list


class Brewery(BaseModel):
    id: int
    name: str
    related_wikipedia_title: str = None
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


def get_breweries() -> List[Brewery]:
    p = pathlib.Path("fixtures/breweries.json")
    list_brews = json.loads(p.read_text())
    brew_list = []
    for brew_data in list_brews:
        brew_list.append(Brewery(**brew_data))

    return brew_list


class UIModel:
    __registered_models = []

    kind: BaseModel.__class__

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.__registered_models.append(cls)

    @classmethod
    def get_registered_models(cls):
        return cls.__registered_models


class PydanticUI:
    registered_models: List[UIModel]
    theme: str

    def __init__(self):
        self.registered_models = UIModel.get_registered_models()

    def list_models(self):
        return self.registered_models

    def get_models_name(self):
        return [model.__name__ for model in self.registered_models]

    def get_model_by_name(self, name: str) -> UIModel:
        for model in self.registered_models:
            if model.__name__ == name:
                return model


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
