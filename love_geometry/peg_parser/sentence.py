from __future__ import annotations
from pypeg2 import List, some

import love_geometry.peg_parser.consts as consts

from .parser_namespaces import ExtendedNamespace
from .love_case import LoveCase


class Sentence(ExtendedNamespace):
    grammar = some(LoveCase), consts.SENTENCE_SEPARATOR

    def __eq__(self, other):
        if self.keys() != other.keys():
            return False

        for name, love_case in other.items():
            if name in self and self[name] == love_case:
                return True

        return False


class LoveStory(List):
    grammar = some(Sentence)
