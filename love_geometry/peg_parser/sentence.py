from __future__ import annotations
from pypeg2 import List, some

import love_geometry.peg_parser.consts as consts

from .parser_namespaces import ExtendedNamespace
from .love_case import LoveCase


class Sentence(ExtendedNamespace):
    VALIDATION_ENABLED = False
    grammar = some(LoveCase), consts.SENTENCE_SEPARATOR

    def __init__(self, *args, **kwargs):
        kwargs["love_case"] = LoveCase
        kwargs["validate_love_stories"] = self.is_validation_enabled()
        super().__init__(*args, **kwargs)

    @classmethod
    def is_validation_enabled(cls):
        return cls.VALIDATION_ENABLED


class LoveStory(List):
    grammar = some(Sentence)

