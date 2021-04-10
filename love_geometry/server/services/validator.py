from __future__ import annotations
import itertools

from love_geometry.server.exceptions import ValidationError

from ..consts import ALLOW_FEELINGS_TO_ITSELF


class LoveStoryValidator:
    def __init__(self, validate_data: bool):
        self._validate_data = validate_data

    def validate(self, parsed_love_story):
        if not self._validate_data:
            return

        self.check_for_duplicated_sentence(parsed_love_story)
        self.check_for_duplicated_love_case(parsed_love_story)

    @staticmethod
    def check_for_duplicated_sentence(parsed_love_story):
        for a, b in itertools.combinations(parsed_love_story, 2):
            if a == b:
                raise ValidationError(f"duplicated sentence: {a}")

    def check_for_duplicated_love_case(self, parsed_love_story):
        for sentence in parsed_love_story:
            self._check_for_relationship_to_itself(sentence)
            self._check_for_duplicated_relationship(sentence)

    @staticmethod
    def _check_for_relationship_to_itself(sentence):
        for origin_name, love_case in list(sentence.items()):
            for feeling, people in love_case.items():
                if origin_name in people and not ALLOW_FEELINGS_TO_ITSELF:
                    raise ValidationError(f"feelings to itself are not permitted")

    @staticmethod
    def _check_for_duplicated_relationship(sentence):
        for origin_name, love_case in list(sentence.items()):
            if len(set(love_case.values())) != len(list(love_case.values())):
                raise ValidationError(f"duplicated relationship: {origin_name} - {list(love_case.values())}")

            for people in love_case.values():
                if len(people) != len(set(people)):
                    raise ValidationError(f"duplicated relationship: {origin_name} - {list(love_case.values())}")

    @staticmethod
    def find_cheaters(sentence: dict) -> list:
        graphs = list(sentence.values())
        cheaters = list()
        for i, graph in enumerate(graphs):
            for edge in graph.edges:
                if any(g.has_edge(*edge) for g in graphs[i + 1:]):
                    cheaters.append(edge[0])

        return cheaters
