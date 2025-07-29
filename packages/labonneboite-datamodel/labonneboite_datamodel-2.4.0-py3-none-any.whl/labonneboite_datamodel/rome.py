from typing import Optional

from pydantic import field_validator
from sqlmodel import Field

from .base import BaseMixin
from .validators import valid_is_naf, valid_is_rome


class Rome(BaseMixin, table=True):
    """This table hosts ROME definitions

    Attributes:
        id:
        rome:
        domain:
        granddomain:
        appellation: Real searchable name for the rome (multiple lines)
        label_granddomain:
        label_domain:
        label_rome:

    """

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)

    rome: str
    domain: Optional[str] = Field(default=None, nullable=False)
    granddomain: Optional[str] = Field(default=None, nullable=False)

    label_rome: str
    label_domain: Optional[str] = Field(default=None, nullable=False)
    label_granddomain: Optional[str] = Field(default=None, nullable=False)

    designation: str

    @field_validator("rome", mode="before")
    @classmethod
    def is_rome(cls, v):
        return valid_is_rome(v)


class RomeNaf(BaseMixin, table=True):
    """This table hosts the mapping between ROME and NAF to be able to make a ROME search correspond to a SIRET

    Attributes:
        id:
        rome: rome code
        naf: naf code
        ratio: Percentage of rome contribution in current naf

    """

    id: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    rome: str
    naf: str
    ratio: float = Field(ge=0, le=100)

    @field_validator("naf", mode="before")
    @classmethod
    def is_naf(cls, v):
        return valid_is_naf(v)

    @field_validator("rome", mode="before")
    @classmethod
    def is_rome(cls, v):
        return valid_is_rome(v)
