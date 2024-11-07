from __future__ import annotations

from collections import namedtuple
from enum import Enum


class AllocationStrategy(Enum):
    STANDARD = "standard"
    D_CHOICE = "d-choice"
    BETA_CHOICE = "beta-choice"


class Trial(namedtuple("Trial", ["allocation_strat", "balls", "bins", "d", "beta"], defaults=(None,) * 5)):

    allocation_strat: AllocationStrategy | None
    balls: int | None
    bins: int | None
    d: float | None
    beta: float | None
