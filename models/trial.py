from __future__ import annotations

from collections import namedtuple
from enum import Enum

FIELDS = ["allocation_strat", "balls", "bins", "d", "beta", "T"]


class AllocationStrategy(Enum):
    STANDARD = "standard"
    D_CHOICE = "d-choice"
    BETA_CHOICE = "beta-choice"


class Trial(namedtuple("Trial", field_names=FIELDS, defaults=(None,) * len(FIELDS))):

    allocation_strat: AllocationStrategy | None
    balls: int | None
    bins: int | None
    d: float | None
    beta: float | None
    T: int | None
