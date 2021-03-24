from __future__ import annotations
from pypeg2 import Namespace, Symbol, optional, name

import love_geometry.peg_parser.consts as consts

from .people import People


class LoveCase(Namespace):
    grammar = name(), People, optional(consts.LOVE_CASE_SEPARATORS)

    @staticmethod
    def generate_persons_love_case(person1: str, person2: str, feeling: str) -> LoveCase:
        return LoveCase(
            [Symbol(feeling), People([person2], name=Symbol(feeling))],
            name=Symbol(person1)
        )
