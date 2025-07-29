from enum import StrEnum, auto
from typing import NotRequired, TypedDict

from noos_inv import exceptions


class PodConfig(TypedDict):
    podNamespace: str
    podPrefix: str
    podPort: int
    localPort: int
    localAddress: NotRequired[str]


type PodsConfig = dict[str, PodConfig]


class ValidatedEnum(StrEnum):
    """Specific Enum with a validated getter method."""

    @classmethod
    def get(cls, value: str) -> StrEnum:
        if value not in cls:
            raise exceptions.UndefinedVariable(f"Unknown {cls.__name__} {value}")
        return cls(value)


class UserType(StrEnum):
    AWS = "AWS"


class InstallType(ValidatedEnum):
    PIPENV = auto()
    POETRY = auto()
    UV = auto()


class GroupType(ValidatedEnum):
    UNIT = auto()
    INTEGRATION = auto()
    FUNCTIONAL = auto()


class FormatterType(ValidatedEnum):
    BLACK = auto()
    ISORT = auto()
    RUFF = auto()


class LinterType(ValidatedEnum):
    BLACK = auto()
    ISORT = auto()
    PYDOCSTYLE = auto()
    FLAKE8 = auto()
    RUFF = auto()
    MYPY = auto()
    IMPORTS = auto()
