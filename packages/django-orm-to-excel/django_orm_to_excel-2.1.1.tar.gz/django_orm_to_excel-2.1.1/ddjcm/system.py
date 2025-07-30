import typing as t
from dataclasses import dataclass

USP: t.TypeAlias = dict[str, t.Any]


@dataclass
class System:
    subsystems: USP
    roles: USP
    entities: USP
