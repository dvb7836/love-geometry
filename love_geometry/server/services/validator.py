from __future__ import annotations
from typing import Optional
import itertools

from love_geometry.server.exceptions import ValidationError


class LoveStoryValidator:
    @staticmethod
    def check_for_duplicated_sentences(sentences: list):
        for sentence1, sentence2 in itertools.combinations(sentences, 2):
            has_duplicated_sentences = sentence1.get("data") == sentence2.get("data")

            if has_duplicated_sentences:
                raise ValidationError("Love story has duplicated sentences")

    @staticmethod
    def find_cheaters(sentence: dict) -> list:
        graphs = list(sentence.values())
        cheaters = list()
        for i, graph in enumerate(graphs):
            for edge in graph.edges:
                if any(g.has_edge(*edge) for g in graphs[i + 1:]):
                    cheaters.append(edge[0])

        return cheaters

    @staticmethod
    def check_for_duplicate(name1, name2, feeling: str, key: str = None):
        if key:
            if name2 in name1:
                return f"Duplicated love case: `{key} {feeling} {name2}`"

        if name1 == name2:
            return f"Duplicated love case: `{name1} {feeling} {name2}`"

        return False
