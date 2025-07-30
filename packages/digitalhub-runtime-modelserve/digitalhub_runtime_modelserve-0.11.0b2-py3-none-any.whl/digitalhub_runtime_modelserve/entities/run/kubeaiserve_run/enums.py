from __future__ import annotations

from enum import Enum


class LoadBalancingStrategy(Enum):
    LEAST_LOAD = "LeastLoad"
    PREFIX_HASH = "PrefixHash"
