from .. import Naf
from pytest import raises


def _get_valid_naf() -> dict:
    return {
        "naf": "1234Z",
        "label": "Something",
    }

# valid job

def test_naf_valid() -> None:
    data = _get_valid_naf()
    assert Naf.validate(data).naf == "1234Z"

# invalid naf

def test_naf_naf_invalid() -> None:
    data = _get_valid_naf()

    for value in ["1f", "0", "abc2", "123f5", "f2345"]:

        data["naf"] = value

        with raises(ValueError):
            Naf.validate(data)
