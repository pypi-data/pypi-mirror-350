from typing import Optional

from pydantic import field_validator
from sqlmodel import Field

from .base import BaseMixin
from .validators import valid_is_naf


class Naf(BaseMixin, table=True):
    """This table hosts the Naf labels

    Attributes:
        id:
        naf: Naf code
        label: Naf description
    """

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)

    naf: str
    label: str

    @field_validator("naf", mode="before")
    @classmethod
    def is_naf(cls, v):
        return valid_is_naf(v)
