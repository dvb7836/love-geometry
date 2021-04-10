from __future__ import annotations
from pypeg2 import Namespace, optional, name

import love_geometry.peg_parser.consts as consts

from .people import People


class LoveCase(Namespace):
    grammar = name(), People, optional(consts.LOVE_CASE_SEPARATORS)

    def __eq__(self, other):
        if self.keys() != other.keys():
            return False

        if list(self.values()) != list(other.values()):
            return False

        return True
