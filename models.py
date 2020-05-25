import datetime
import enum
import json
import pathlib
from typing import List

from pydantic import BaseModel


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
