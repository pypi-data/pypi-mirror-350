from collections import defaultdict
from datetime import datetime
from typing import Any, TypeAlias, TypedDict

import lazy_import
import orjson
from anystore.util import clean_dict
from banal import is_mapping
from followthemoney import model
from followthemoney.util import join_text
from ftmq.types import SDict
from ftmq.util import clean_string, make_proxy
from nomenklatura.entity import CE, CompositeEntity
from normality import collapse_spaces
from pydantic import BaseModel, create_model, field_validator, model_validator
from rigour.addresses import clean_address, format_address_line, normalize_address

from ftm_geocode.cache import make_cache_key
from ftm_geocode.nuts import get_nuts
from ftm_geocode.settings import GEOCODERS, Settings
from ftm_geocode.util import (
    clean_country_codes,
    clean_country_names,
    get_country_code,
    get_first,
)

settings = Settings()
USE_LIBPOSTAL = settings.libpostal


class GeocodingResult(BaseModel):
    cache_key: str
    address_id: str
    original_line: str
    result_line: str
    country: str
    lon: float
    lat: float
    geocoder: str
    geocoder_place_id: str | None = None
    geocoder_raw: dict[str, Any] | None = None
    nuts1_id: str | None = None
    nuts2_id: str | None = None
    nuts3_id: str | None = None
    ts: datetime | None = None

    @property
    def nuts(self) -> tuple[str, str, str] | None:
        if self.nuts1_id:
            return (self.nuts1_id, self.nuts2_id, self.nuts3_id)

    def apply_nuts(self) -> None:
        if not self.nuts1_id or not self.nuts2_id or not self.nuts3_id:
            nuts = get_nuts(self.lon, self.lat)
            if nuts is not None:
                self.nuts1_id = nuts.nuts1_id
                self.nuts2_id = nuts.nuts2_id
                self.nuts3_id = nuts.nuts3_id

    def to_proxy(self) -> CE:
        address = Address.from_result(self)
        proxy = address.to_proxy()
        proxy.add("region", self.nuts)
        return proxy

    @model_validator(mode="before")
    @classmethod
    def make_cache_key(cls, data: SDict) -> SDict:
        data["cache_key"] = make_cache_key(
            data["original_line"], country=data.get("country")
        )
        return data

    @field_validator("geocoder_place_id", mode="before")
    @classmethod
    def to_str(cls, value) -> str | None:
        return clean_string(value)

    @field_validator("geocoder_raw", mode="before")
    @classmethod
    def to_dict(cls, value: Any) -> dict[str, Any]:
        if is_mapping(value):
            return value
        if isinstance(value, (str, bytes)):
            return orjson.loads(value)
        return {}


# https://github.com/openvenues/libpostal#parser-labels
# postal -> ftm
# FIXME extend ftm schema to align with postal output?
MAPPING = (
    ("full", "full"),  # used as dummy prop when USE_LIBPOSTAL=False
    # venue name e.g. "Brooklyn Academy of Music", and building names
    # e.g. "Empire State Building"
    ("house", "remarks"),
    # for category queries like "restaurants", etc.
    ("category", "keywords"),
    # phrases like "in", "near", etc. used after a category phrase to help with parsing
    # queries like "restaurants in Brooklyn"
    ("near", "remarks"),
    # usually refers to the external (street-facing) building number. In some countries
    # this may be a compound, hyphenated number which also includes an apartment number,
    # or a block number (a la Japan), but libpostal will just call it the house_number
    # for simplicity.
    ("house_number", "remarks"),
    # street name(s)
    ("road", "street"),
    # an apartment, unit, office, lot, or other secondary unit designator
    ("unit", "remarks"),
    # expressions indicating a floor number e.g. "3rd Floor", "Ground Floor", etc.
    ("level", "remarks"),
    # numbered/lettered staircase
    ("staircase", "remarks"),
    # numbered/lettered entrance
    ("entrance", "remarks"),
    # post office box: typically found in non-physical (mail-only) addresses
    ("po_box", "postOfficeBox"),
    # postal codes used for mail sorting
    ("postcode", "postalCode"),
    # usually an unofficial neighborhood name like "Harlem", "South Bronx", or
    # "Crown Heights"
    ("suburb", "remarks"),
    # these are usually boroughs or districts within a city that serve some official
    # purpose e.g. "Brooklyn" or "Hackney" or "Bratislava IV"
    ("city_district", "remarks"),
    # any human settlement including cities, towns, villages, hamlets, localities, etc.
    ("city", "city"),
    # named islands e.g. "Maui"
    ("island", "region"),
    # usually a second-level administrative division or county.
    ("state_district", "region"),
    # a first-level administrative division. Scotland, Northern Ireland, Wales, and
    # England in the UK are mapped to "state" as well (convention used in OSM,
    # GeoPlanet, etc.)
    ("state", "state"),
    # informal subdivision of a country without any political status
    ("country_region", "region"),
    # sovereign nations and their dependent territories, anything with an ISO-3166 code.
    ("country", "country"),
    ("country_code", "country"),
    # currently only used for appending “West Indies” after the country name, a pattern
    # frequently used in the English-speaking Caribbean e.g. “Jamaica, West Indies”
    ("world_region", "region"),
)

POSTAL_KEYS = [m[0] for m in MAPPING]

Values = list[str] | None


class PostalContext(TypedDict):
    language: str | None
    country: str | None


class AddressBase(BaseModel):
    def get_country(self) -> str:
        return ";".join(self.country or [])

    def get_first(self, attr, default: Any | None = None) -> str | None:
        return get_first(getattr(self, attr, None), default)

    def get_id(self) -> str:  # serves as cache key
        line = normalize_address(self.get_formatted_line(), latinize=True)
        key = make_cache_key(line, country=self.get_first("country"))
        assert key is not None
        return key

    def to_dict(self) -> dict[str, list[str]]:
        return clean_dict(self.model_dump())


class PostalAddressBase(AddressBase):
    full: Values = None
    country_code: Values = None

    def __init__(self, **data):
        data["country"] = clean_country_names(data.get("country"))
        data["country_code"] = clean_country_codes(data.get("country"))
        super().__init__(**data)

    def get_formatted_line(self) -> str:
        country = self.get_first("country")
        data = {
            "attention": self.get_first("near"),
            "house": join_text(self.get_first("house"), self.get_first("po_box")),
            "house_number": self.get_first("house_number"),
            "road": self.get_first("street") or self.get_first("road"),
            "postcode": self.get_first("postcode"),
            "city": self.get_first("city"),
            "state": self.get_first("state"),
            "country": country,
        }
        return format_address_line(data, country=country)

    def to_dict(self) -> dict[str, str]:
        return clean_dict({k: get_first(v) for k, v in self.model_dump().items()})

    @classmethod
    def from_postal_result(
        cls, input_data: list[tuple[str, str]], **ctx: PostalContext
    ) -> "PostalAddress":
        data = defaultdict(set)
        for value, key in input_data:
            data[key].add(value.title())
        if "country" in ctx:
            data["country"].add(ctx["country"])
        return cls(**data)

    @classmethod
    def from_string(cls, value: str, **ctx: PostalContext) -> "PostalAddress":
        value = clean_address(value)
        if USE_LIBPOSTAL:
            parse_address = lazy_import.lazy_callable("postal.parser.parse_address")
            # postal screams if language or country is None
            ctx = {k: ctx.get(k, "") or "" for k in ("language", "country")}
            result = parse_address(value, **ctx)
        else:
            result = [(value, "full")]
        return cls.from_postal_result(result, **ctx)


PostalAddress: PostalAddressBase = create_model(
    "PostalAddress",
    **{k: (Values, None) for k in POSTAL_KEYS},
    __base__=PostalAddressBase,
)

FtmAddressBase: AddressBase = create_model(
    "FtmAddressBase",
    **{p: (Values, None) for p in model.get("Address").properties},
    __base__=AddressBase,
)


class Address(FtmAddressBase):
    _id: str | None = None
    _postal: PostalAddress | None = None

    def get_id(self) -> str:
        # use place ids to generate ids
        if self._id:
            return self._id
        osmId, googlePlaceId = self.get_first("osmId"), self.get_first("googlePlaceId")
        if osmId:
            return f"addr-osm-{osmId}"
        if googlePlaceId:
            return f"addr-google-{googlePlaceId}"
        return super().get_id()

    def to_proxy(self) -> CE:
        proxy = make_proxy(
            {
                "id": self.get_id(),
                "schema": "Address",
                "properties": clean_dict(self.model_dump()),
            }
        )
        proxy.set("full", self.get_formatted_line())
        return proxy

    def get_formatted_line(self) -> str:
        country = get_country_code(self.get_first("country"))
        data = {
            "attention": collapse_spaces(
                " ".join((self.get_first("summary", ""), " ".join(self.remarks or [])))
            ),
            "house": self.get_first("postOfficeBox"),
            "road": self.get_first("road")
            or self.get_first("street")
            or self.get_first("full"),
            "postcode": self.get_first("postalCode"),
            "city": self.get_first("city"),
            "state": self.get_first("state"),
        }
        return format_address_line(data, country=country)

    @classmethod
    def from_postal(cls, input_data: PostalAddress, **ctx: PostalContext) -> "Address":
        mapping = dict(MAPPING)
        data = defaultdict(set)
        data["country"].add(ctx.get("country"))
        for key, values in input_data:
            if key == "country_code":
                key = "country"
            if values is not None:
                data[mapping[key]].update(values)
        data["country"] = clean_country_codes(data["country"])
        instance = cls(**data)
        instance._postal = input_data
        return instance

    @classmethod
    def from_string(cls, value: str, **ctx: PostalContext) -> "Address":
        value = clean_address(value)
        return cls.from_postal(PostalAddress.from_string(value, **ctx))

    @classmethod
    def from_result(cls, result: GeocodingResult) -> "Address":
        ctx = {"country": result.country}
        address = cls.from_postal(PostalAddress.from_string(result.result_line, **ctx))
        address.full = [result.result_line]
        address.longitude = [str(result.lon)]
        address.latitude = [str(result.lat)]
        if result.geocoder == GEOCODERS.nominatim.name:
            address.osmId = [result.geocoder_place_id]
        if result.geocoder == GEOCODERS.google.name:
            address.googlePlaceId = [result.geocoder_place_id]
        return address

    @classmethod
    def from_proxy(cls, proxy: CE) -> "Address":
        data = proxy.to_dict()
        address = cls(**data["properties"])
        address._id = proxy.id
        return address


AddressInput: TypeAlias = str | Address | PostalAddress | CE | GeocodingResult


def get_address(
    data: AddressInput, address_id: str | None = None, **ctx: PostalContext
) -> Address:
    if isinstance(data, str):
        addr = Address.from_string(data, **ctx)
    elif isinstance(data, PostalAddress):
        addr = Address.from_postal(data, **ctx)
    elif isinstance(data, CompositeEntity):
        addr = Address.from_proxy(data)
    elif isinstance(data, GeocodingResult):
        addr = Address.from_result(data)
    else:
        raise ValueError(f"Invalid input format: {data}")
    if address_id is not None:
        addr._id = address_id
    return addr


def get_components(data: AddressInput, **ctx: PostalContext) -> dict[str, str | None]:
    if isinstance(data, PostalAddress):
        return data.to_dict()
    if isinstance(data, Address):
        return data._postal.to_dict()

    if isinstance(data, str):
        data = PostalAddress.from_string(data, **ctx)
    elif isinstance(data, CompositeEntity):
        data = PostalAddress.from_string(data.caption, **ctx)
    elif isinstance(data, GeocodingResult):
        data = PostalAddress.from_string(GeocodingResult.result_line, **ctx)
    else:
        raise NotImplementedError(data)

    return data.to_dict()


def get_formatted_line(data: AddressInput, **ctx: PostalContext) -> str:
    address = get_address(data, **ctx)
    return address.get_formatted_line()


def get_canonical_id(geocoder: GEOCODERS, place_id: str) -> str:
    if geocoder == GEOCODERS.nominatim:
        return f"addr-osm-{place_id}"
    return f"addr-{geocoder.value}-{place_id}"


def get_coords(data: AddressInput, **ctx: PostalContext) -> tuple[float, float] | None:
    address = get_address(data, **ctx)
    try:
        return float(get_first(address.longitude)), float(get_first(address.latitude))
    except ValueError:
        return None
