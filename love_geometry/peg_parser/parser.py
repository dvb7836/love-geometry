from __future__ import annotations
from pypeg2 import Namespace, Symbol, Enum, K, List, flag, attr, optional, name, some

import love_geometry.peg_parser.consts as consts
from love_geometry.peg_parser.parser_namespaces import ExtendedNamespace


class Feeling(Symbol):
    grammar = Enum(*(K(f"{feeling}") for feeling in consts.FEELINGS))


class Person(str):
    grammar = str


class People(List):
    mutually = consts.DOUBLE_ENDED_RELATIONSHIP_FLAG_KEYWORD
    grammar = flag(mutually, K(mutually)), attr("name", Feeling), Person


class LoveCase(Namespace):
    grammar = name(), People, optional(consts.LOVE_CASE_SEPARATORS)

    @staticmethod
    def generate_persons_love_case(person1: str, person2: str, feeling: str) -> LoveCase:
        return LoveCase(
            [Symbol(feeling), People([person2], name=Symbol(feeling))],
            name=Symbol(person1)
        )


class Sentence(ExtendedNamespace):
    grammar = some(LoveCase), consts.SENTENCE_SEPARATOR

    def __init__(self, *args, **kwargs):
        kwargs["love_case"] = LoveCase
        super().__init__(*args, **kwargs)


class LoveStory(List):
    grammar = some(Sentence)
