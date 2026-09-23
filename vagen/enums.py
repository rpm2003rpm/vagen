"""Shared enumerations for vagen."""

from enum import Enum
from typing import Tuple

class PortDirection(str, Enum):
    """Verilog-A port direction."""

    INPUT = "input"
    OUTPUT = "output"
    INOUT = "inout"
    INTERNAL = "internal"

    @classmethod
    def values(cls) -> Tuple[str, ...]:
        return tuple(item.value for item in cls)


class CrossEdge(str, Enum):
    """Cross event edge selection."""

    RISING = "rising"
    FALLING = "falling"
    BOTH = "both"

    @classmethod
    def values(cls) -> Tuple[str, ...]:
        return tuple(item.value for item in cls)
