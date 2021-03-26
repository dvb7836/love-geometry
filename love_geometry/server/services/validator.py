from __future__ import annotations
import itertools

from love_geometry.server.exceptions import ValidationError
from pypeg2.xmlast import create_tree
from xmldiff import main

from ..consts import ALLOW_FEELINGS_TO_ITSELF


class LoveStoryValidator:

    def validate(self, parsed_love_story):
        self.check_for_duplicated_sentence(parsed_love_story)
        self.check_for_duplicated_love_case(parsed_love_story)

    @staticmethod
    def check_for_duplicated_sentence(parsed_love_story):
        xml_tree = create_tree(parsed_love_story)

        sentences = xml_tree.findall('Sentence')
        if len(sentences) > 1:
            for sentence1, sentence2 in itertools.combinations(sentences, 2):
                if not main.diff_trees(sentence1, sentence2):
                    raise ValidationError(f"duplicated sentences")

    @staticmethod
    def check_for_duplicated_love_case(parsed_love_story):
        for sentence in parsed_love_story:
            for origin_name, love_case in list(sentence.items()):
                for feeling, people in love_case.items():
                    if origin_name in people and not ALLOW_FEELINGS_TO_ITSELF:
                        raise ValidationError(f"feelings to itself are not permitted")

    @staticmethod
    def find_cheaters(sentence: dict) -> list:
        graphs = list(sentence.values())
        cheaters = list()
        for i, graph in enumerate(graphs):
            for edge in graph.edges:
                if any(g.has_edge(*edge) for g in graphs[i + 1:]):
                    cheaters.append(edge[0])

        return cheaters
