import os
from ..base import is_sqlite, BaseMixin
from unittest.mock import patch


@patch.dict(os.environ, {"IS_SQLITE": "true"}, clear=True)
def test_sqlite_true():

    base = BaseMixin()
    assert is_sqlite() is True
    assert base.last_modified is not None


@patch.dict(os.environ, {"IS_SQLITE": "false"}, clear=True)
def test_sqlite_false():

    base = BaseMixin()
    assert is_sqlite() is False
    assert base.last_modified is not None
