import pandas as pd
from pytest import raises

from .. import Office


def _get_valid_office() -> dict:
    return {
        "siret": "12346578901234",
        "naf": "1234Z",
        "company_name": "Nintendo",
        "office_name": "Mario 3",
    }


# valid office


def test_office_valid() -> None:
    data = _get_valid_office()
    assert Office.validate(data).siret == "12346578901234"


# invalid siret


def test_siret_valid() -> None:
    data = _get_valid_office()
    data["siret"] = "1".zfill(9)
    assert Office.validate(data).siret == "1".zfill(14)


def test_siret_invalid() -> None:
    data = _get_valid_office()
    data["siret"] = "1".zfill(8) + "abc"

    with raises(ValueError):
        Office.validate(data)


# invalid naf


def test_naf_invalid() -> None:
    data = _get_valid_office()

    for value in ["1".zfill(5), "0".zfill(4), "abc2".zfill(5)]:

        data["naf"] = value

        with raises(ValueError):
            Office.validate(data)


# phone


def test_phone_invalid() -> None:
    data = _get_valid_office()
    data["phone"] = "1".zfill(8)

    with raises(ValueError):
        Office.validate(data)

    for value in [None, ""]:
        data["phone"] = value
        assert Office.validate(data).phone == ""


def test_phone_valid() -> None:
    data = _get_valid_office()
    data["phone"] = "1".zfill(9)
    assert Office.validate(data).phone == "1".zfill(10)


# headcount_range


def test_headcount_range_invalid() -> None:
    data = _get_valid_office()

    for value in ["1", "10-5", "00000"]:

        data["headcount_range"] = value

        assert Office.validate(data).headcount_range == ""


def test_headcount_range_valid() -> None:
    data = _get_valid_office()
    data["headcount_range"] = "1-2"

    assert Office.validate(data).headcount_range == "1-2"


# citycode


def test_postcode_invalid() -> None:
    data = _get_valid_office()

    for value in ["1234", "abc14", "00000"]:

        data["postcode"] = value

        with raises(ValueError):
            Office.validate(data)


def test_postcode_valid() -> None:
    data = _get_valid_office()
    data["postcode"] = "75014"
    assert Office.validate(data).postcode == "75014"

    data["postcode"] = None
    assert Office.validate(data).postcode == ""

    data["postcode"] = ""
    assert Office.validate(data).postcode == ""


# citycode


def test_citycode_invalid() -> None:
    data = _get_valid_office()

    for value in ["1234", "00000"]:

        data["citycode"] = value

        with raises(ValueError):
            Office.validate(data)


def test_citycode_valid() -> None:
    data = _get_valid_office()
    data["citycode"] = "75014"
    assert Office.validate(data).citycode == "75014"

    data["citycode"] = "2B014"
    assert Office.validate(data).citycode == "2B014"

    data["citycode"] = None
    assert Office.validate(data).citycode == ""

    data["citycode"] = ""
    assert Office.validate(data).citycode == ""


# problems due to pandas


def test_pandas_null() -> None:

    with pd.read_csv(
        "./labonneboite_datamodel/tests/data/test.csv",
        delimiter=";",
        chunksize=10,
        keep_default_na=False,
        on_bad_lines="warn",
    ) as reader:
        for chunk in reader:

            chunk["siret"] = chunk["siret"].astype(str)
            chunk["tel"] = chunk["tel"].astype(str)
            chunk["trancheeffectif"] = chunk["trancheeffectif"].astype(str)
            chunk["codepostal"] = chunk["codepostal"].astype(str)
            chunk["codecommune"] = chunk["codecommune"].astype(str)

            # formatting
            chunk["siret"] = chunk["siret"].str.zfill(14)
            chunk["tel"] = chunk["tel"].str.zfill(10)
            chunk["codepostal"] = chunk["codepostal"].str.zfill(5)
            chunk["codecommune"] = chunk["codecommune"].str.zfill(5)

            for _, row in chunk.iterrows():

                data = {
                    "siret": row["siret"],
                    "naf": row["codenaf"],
                    "company_name": row["raisonsociale"],
                    "office_name": row["enseigne"],
                    "streetnumber": row["numerorue"],
                    "street": row["libellerue"],
                    "postcode": row["codepostal"],
                    "citycode": row["codecommune"],
                    "headcount_range": row["trancheeffectif"],
                    "email": row["email"],
                    "website": row["website"],
                    "phone": row["tel"],
                }

            assert Office.validate(data).siret != ""


def test_invalid_email() -> None:

    data = _get_valid_office()
    data["email"] = "NULL"
    assert Office.validate(data).email == ""

    data["email"] = "noone.@nowhere.com"
    assert Office.validate(data).email == ""

    data["email"] = "no+one@nowhere.com"
    assert Office.validate(data).email == "no+one@nowhere.com"

    data["email"] = "noone@nowherecom"
    assert Office.validate(data).email == ""
