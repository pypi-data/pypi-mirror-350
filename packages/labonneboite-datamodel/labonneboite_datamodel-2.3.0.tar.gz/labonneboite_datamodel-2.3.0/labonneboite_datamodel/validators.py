import re


def valid_is_naf(v):
    """Validator for `naf`

    Rules:
        - should be 5 characters long
        - the first 4 values should be numeric
        - The last value should be a letter

    Raises:
        ValueError:

    """
    # A valid NAF is composed 4 numbers and a letter (could be a regex ^\d{4}\D{1}$)
    error = "a NAF should be made up of 4 numbers and a letter"
    pattern = r"^\d{4}\D$"

    if not re.match(pattern, v):
        raise ValueError(error)

    return v


def valid_is_rome(v):
    """Validator for `naf`

    Rules:
        - should be 5 characters long
        - the first 4 values should be numeric
        - The last value should be a letter

    Raises:
        ValueError:

    """
    # A valid NAF is composed 4 numbers and a letter (could be a regex ^\d{4}\D{1}$)
    error = "a NAF should be made up of 4 numbers and a letter"
    pattern = r"^\D\d{4}"

    if not re.match(pattern, v):
        raise ValueError(error)

    return v
