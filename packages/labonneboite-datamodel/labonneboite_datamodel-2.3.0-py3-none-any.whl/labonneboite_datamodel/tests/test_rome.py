from unittest import TestCase
from .. import RomeNaf, Rome
from pytest import raises


def _get_valid_rome() -> dict:
    return {
        "rome": "M1234",
        "label_rome": "Something",
        "designation": "Some work i do"
    }


def _get_valid_romenaf() -> dict:
    return {
        "rome": "M1234",
        "naf": "1234Z",
        "ratio": 75.5
    }

# valid rome


def test_rome_valid() -> None:
    data = _get_valid_rome()
    assert Rome.validate(data).rome == "M1234"


def test_naf_valid() -> None:
    data = _get_valid_romenaf()
    assert RomeNaf.validate(data).naf == "1234Z"

# invalid naf


def test_rome_invalid() -> None:
    data = _get_valid_rome()

    for value in ["1f100", "0", "abc2", "12345", "1234F"]:

        data["rome"] = value

        with raises(ValueError):
            Rome.validate(data)


def test_romenaf_invalid() -> None:
    data = _get_valid_romenaf()

    for value in ["1f", "0", "abc2", "123f5", "1234F"]:

        data["rome"] = value

        with raises(ValueError):
            RomeNaf.validate(data)

    for value in ["1f", "0", "abc2", "123f5", "f2345"]:

        data["naf"] = value

        with raises(ValueError):
            RomeNaf.validate(data)

    for value in [-1, 101]:
        data["ratio"] = value

        with raises(ValueError):
            RomeNaf.validate(data)
