from typing import Protocol
from dataclasses import dataclass


class Limit(Protocol):
    name: str

    def validate(self, value: int) -> None:
        """RuntimeError :raise if not valid"""


@dataclass
class Enum(Limit):
    name: str
    values: tuple[int, ...]

    def validate(self, value: int) -> None:
        if value not in self.values:
            raise RuntimeError(F"for {self.name} got {value}, expected {self.values}")


@dataclass
class MinMax(Limit):
    name: str
    min: int
    max: int

    def validate(self, value: int) -> None:
        if (
            self.min > value
            or self.max < value
        ):
            raise RuntimeError(F"for {self.name} got {value}, expected ({self.min}..{self.max})")
