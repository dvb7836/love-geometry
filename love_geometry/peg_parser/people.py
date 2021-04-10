from __future__ import annotations
from pypeg2 import K, List, flag, attr

import love_geometry.peg_parser.consts as consts

from .base import Feeling


class People(List):
    mutually = consts.DOUBLE_ENDED_RELATIONSHIP_FLAG_KEYWORD
    grammar = flag(mutually, K(mutually)), attr("name", Feeling), str

    def __eq__(self, other):
        if list(self) == list(other):
            return True

        return False

    def __hash__(self):
        return hash(tuple(self))
