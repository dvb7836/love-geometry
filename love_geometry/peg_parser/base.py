from __future__ import annotations
from pypeg2 import Symbol, Enum, K

import love_geometry.peg_parser.consts as consts


class Feeling(Symbol):
    grammar = Enum(*(K(f"{feeling}") for feeling in consts.FEELINGS))
