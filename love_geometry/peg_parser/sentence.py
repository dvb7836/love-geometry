from __future__ import annotations
from pypeg2 import List, some

import love_geometry.peg_parser.consts as consts

from .parser_namespaces import ExtendedNamespace
from .love_case import LoveCase


class Sentence(ExtendedNamespace):
    grammar = some(LoveCase), consts.SENTENCE_SEPARATOR


class LoveStory(List):
    grammar = some(Sentence)
