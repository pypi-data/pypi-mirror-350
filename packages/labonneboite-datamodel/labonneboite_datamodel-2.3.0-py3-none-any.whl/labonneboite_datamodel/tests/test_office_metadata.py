
from .. import OfficeMetadata
import pandas as pd

from pytest import raises


def _get_valid_metadata() -> dict:
    return {
        "siret": "12346578901234",
        "subscribed": True,
        "hide_phone": False,
        "hide_email": False,
        "hide_location": False,
    }

# valid metadata


def test_OfficeMetadata_valid() -> None:
    data = _get_valid_metadata()
    assert OfficeMetadata.validate(data).siret == "12346578901234"

# invalid siret


def test_siret_valid() -> None:
    data = _get_valid_metadata()
    data["siret"] = "1".zfill(9)
    assert OfficeMetadata.validate(data).siret == "1".zfill(14)


def test_siret_invalid() -> None:
    data = _get_valid_metadata()
    data["siret"] = "1".zfill(8) + "abc"

    with raises(ValueError):
        OfficeMetadata.validate(data)

# invalid naf


def test_naf_invalid() -> None:
    data = _get_valid_metadata()

    data2 = data
    data2["subscribed"] = None
    with raises(ValueError):
        OfficeMetadata.validate(data)

    data2 = data
    data2["hide_phone"] = None
    with raises(ValueError):
        OfficeMetadata.validate(data)

    data2 = data
    data2["hide_email"] = None
    with raises(ValueError):
        OfficeMetadata.validate(data)
    
    data2 = data
    data2["hide_location"] = None
    with raises(ValueError):
        OfficeMetadata.validate(data)
