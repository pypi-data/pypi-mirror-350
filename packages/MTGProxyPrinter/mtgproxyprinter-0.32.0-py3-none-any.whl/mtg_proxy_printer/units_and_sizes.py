#  Copyright © 2020-2025  Thomas Hess <thomas.hess@udo.edu>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program. If not, see <http://www.gnu.org/licenses/>.


"""Contains some constants, type definitions and the unit parsing support code"""
import configparser
import enum
import re
import sqlite3
import typing
try:
    from typing import NotRequired
except ImportError:  # Compatibility with Python < 3.11
    from typing_extensions import NotRequired

import pint
try:
    from pint.facets.plain.registry import QuantityT, UnitT
except ImportError:  # Compatibility with Pint 0.21 for Python 3.8 support
    QuantityT = UnitT = typing.Any
from PyQt5.QtCore import QSize


def _setup_units() -> typing.Tuple[pint.UnitRegistry, QuantityT]:
    registry = pint.UnitRegistry(cache_folder=":auto:")
    resolution = registry.parse_expression("300dots/inch")
    print_context = pint.Context("print")
    print_context.add_transformation("[length]", "[printing_unit]", lambda _, x: x*RESOLUTION)
    print_context.add_transformation("[printing_unit]", "[length]", lambda _, x: x/RESOLUTION)
    registry.add_context(print_context)
    return registry, resolution


unit_registry, RESOLUTION = _setup_units()
DEFAULT_SAVE_SUFFIX = "mtgproxies"

# typing shortcuts
ShouldBeUUID = WEB_URI = API_URI = str
Colors = StringList = typing.List[str]
StringSet = typing.Set[str]
OptStr = typing.Optional[str]
IntList = typing.List[int]
StrDict = typing.Dict[str, str]
T = typing.TypeVar("T")

class SectionProxy(configparser.SectionProxy):
    def get_quantity(self, option: str, fallback: str = None, *, raw=False, vars=None) -> QuantityT:
        raw_value = self.get(option, fallback, raw=raw, vars=vars)
        return unit_registry.parse_expression(raw_value)

class ConfigParser(configparser.ConfigParser):

    __getitem__: typing.Callable[[str], SectionProxy]  # Type hint that [] returns a SectionProxy having get_quantity()

    def get_quantity(self, section: str, option: str, fallback: str = None, *, raw=False, vars=None) -> QuantityT:
        raw_value = self.get(section, option, raw=raw, vars=vars, fallback=fallback)
        return unit_registry.parse_expression(raw_value)


configparser.SectionProxy = SectionProxy
configparser.ConfigParser = ConfigParser


class UUID(str):
    uuid_re = re.compile(r"[a-f0-9]{8}-([a-f0-9]{4}-){3}[a-f0-9]{12}")

    def __new__(cls, *args, **kwargs):
        new = super().__new__(cls, *args, **kwargs)
        if cls.uuid_re.fullmatch(new):
            return new
        raise ValueError(f"Not a proper UUID: '{new}'")


class CardSize(typing.NamedTuple):
    width: QuantityT
    height: QuantityT

    def as_qsize_px(self):
        return QSize(round(self.width.magnitude), round(self.height.magnitude))

    def to_save_data(self):
        return f"{self.width.magnitude:.0f}x{self.height.magnitude:.0f}"


@enum.unique
class CardSizes(CardSize, enum.Enum):
    REGULAR = CardSize(unit_registry("745 pixel"), unit_registry("1040 pixel"))
    OVERSIZED = CardSize(unit_registry("1040 pixel"), unit_registry("1490 pixel"))

    @classmethod
    def for_page_type(cls, page_type: "PageType") -> CardSize:
        return cls.OVERSIZED if page_type == PageType.OVERSIZED else cls.REGULAR

    @classmethod
    def from_bool(cls, value: bool) -> CardSize:
        return cls.OVERSIZED if value else cls.REGULAR


sqlite3.register_adapter(CardSize, lambda item: item.to_save_data())
sqlite3.register_adapter(CardSizes, lambda item: item.to_save_data())

@enum.unique
class PageType(enum.Enum):
    """
    This enum can be used to indicate what kind of images are placed on a Page.
    A page that only contains regular-sized images is REGULAR, a page only containing oversized images is OVERSIZED.
    An empty page has an UNDETERMINED image size and can be used for both oversized or regular sized cards
    A page containing both is MIXED. This should never happen. A page being MIXED indicates a bug in the code.
    """
    UNDETERMINED = enum.auto()
    REGULAR = enum.auto()
    OVERSIZED = enum.auto()
    MIXED = enum.auto()


class ImageUriType(typing.TypedDict):
    small: str
    normal: str
    large: str
    png: str
    art_crop: str
    border_crop: str


class FaceDataType(typing.TypedDict):
    artist: NotRequired[str]
    artist_ids: NotRequired[typing.List[ShouldBeUUID]]
    cmc: NotRequired[float]
    color_indicator: NotRequired[Colors]
    colors: NotRequired[Colors]
    defense: NotRequired[str]
    flavor_text: NotRequired[str]
    illustration_id: NotRequired[ShouldBeUUID]
    image_uris: NotRequired[ImageUriType]
    layout: NotRequired[str]
    loyalty: NotRequired[str]
    mana_cost: str
    name: str
    object: str  # Object type, always constant
    oracle_id: NotRequired[ShouldBeUUID]  # Present in either the faces of reversible cards, or the parent card object otherwise
    oracle_text: NotRequired[str]
    power: NotRequired[str]
    printed_name: NotRequired[str]
    printed_text: NotRequired[str]
    printed_type_line: NotRequired[str]
    toughness: NotRequired[str]
    type_line: NotRequired[str]
    watermark: NotRequired[str]


class RelatedCardType(typing.TypedDict):
    object: str
    id: ShouldBeUUID
    component: str
    name: str
    type_line: str
    uri: str


_CardPreviewFields = typing.TypedDict("_CardPreviewFields", {
    # Note: Requires this syntax, because keys are not valid python identifiers
    "preview.previewed_at": str,
    "preview.source_uri": WEB_URI,
    "preview.source": str,
})


class CardDataType(_CardPreviewFields):
    """Card data type modelled according to https://scryfall.com/docs/api/cards"""

    # Core fields
    arena_id: NotRequired[int]
    id: ShouldBeUUID
    lang: str
    mtgo_id: NotRequired[int]
    mtgo_foil_id: NotRequired[int]
    multiverse_ids: NotRequired[IntList]
    tcgplayer_id: NotRequired[int]
    tcgplayer_etched_id: NotRequired[int]
    cardmarket_id: NotRequired[int]
    object: str  # Object type, always "card"
    layout: str
    oracle_id: NotRequired[ShouldBeUUID]  # Always present, except for "reversible" cards, where this is in the individual faces
    print_search_uri: API_URI
    rulings_uri: API_URI
    scryfall_uri: WEB_URI
    uri: API_URI

    # Gameplay fields
    all_parts: NotRequired[typing.List[RelatedCardType]]
    card_faces: NotRequired[typing.List[FaceDataType]]
    cmc: float
    color_identity: Colors
    color_indicator: NotRequired[Colors]
    colors: NotRequired[Colors]
    defense: NotRequired[str]
    edhrec_rank: NotRequired[int]
    hand_modifier: NotRequired[str]
    keywords: NotRequired[StringList]
    legalities: StrDict
    life_modifier: NotRequired[str]
    loyalty: NotRequired[str]
    mana_cost: NotRequired[str]
    name: str
    oracle_text: NotRequired[str]
    penny_rank: NotRequired[int]
    power: NotRequired[str]
    produced_mana: NotRequired[Colors]
    reserved: bool
    toughness: NotRequired[str]
    type_line: str

    # Print fields
    artist: NotRequired[str]
    artist_ids: NotRequired[typing.List[ShouldBeUUID]]
    attraction_lights: NotRequired[IntList]
    booster: bool
    border_color: str
    card_back_id: ShouldBeUUID
    collector_number: str
    content_warning: NotRequired[bool]
    digital: bool
    finishes: StringList
    flavor_name: NotRequired[str]
    flavor_text: NotRequired[str]
    frame_effects: NotRequired[StringList]
    frame: str
    full_art: bool
    games: StringList
    highres_image: bool
    illustration_id: NotRequired[ShouldBeUUID]
    image_status: str
    image_uris: NotRequired[ImageUriType]
    oversized: bool
    prices: typing.Dict[str, float]
    printed_name: NotRequired[str]
    printed_text: NotRequired[str]
    printed_type_line: NotRequired[str]
    promo: bool
    promo_types: NotRequired[StringList]
    purchase_uris: NotRequired[typing.Dict[str, ShouldBeUUID]]
    rarity: str
    related_uris: typing.Dict[str, WEB_URI]
    released_at: str
    reprint: bool
    scryfall_set_uri: WEB_URI
    set_name: str
    set_search_uri: API_URI
    set_type: str
    set: str  # Set code
    set_id: ShouldBeUUID
    story_spotlight: bool
    textless: bool
    variation: bool
    variation_of: NotRequired[ShouldBeUUID]
    security_stamp: NotRequired[str]
    watermark: NotRequired[str]


class BulkDataType(typing.TypedDict):
    """
    The data returned by the bulk data API end point.
    See https://scryfall.com/docs/api/bulk-data
    """
    id: ShouldBeUUID
    uri: str
    type: str
    name: str
    description: str
    download_uri: str
    updated_at: str
    size: int
    content_type: str
    content_encoding: str
