from __future__ import annotations
import itertools

from love_geometry.server.exceptions import ValidationError
from pypeg2.xmlast import create_tree, xml2thing, thing2xml
from lxml import etree
from xmldiff import main


class LoveStoryValidator:
    @staticmethod
    def validate(parsed_love_story):
        xml_tree = create_tree(parsed_love_story)

        sentences = xml_tree.findall('Sentence')
        if len(sentences) > 1:
            for sentence1, sentence2 in itertools.combinations(sentences, 2):
                if not main.diff_trees(sentence1, sentence2):
                    raise ValidationError(f"duplicated sentences")

    @staticmethod
    def find_cheaters(sentence: dict) -> list:
        graphs = list(sentence.values())
        cheaters = list()
        for i, graph in enumerate(graphs):
            for edge in graph.edges:
                if any(g.has_edge(*edge) for g in graphs[i + 1:]):
                    cheaters.append(edge[0])

        return cheaters
