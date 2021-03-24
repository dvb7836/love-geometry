from __future__ import annotations
from collections import defaultdict
import random
from typing import Dict, Optional, Tuple

import matplotlib.pyplot as plt
import networkx as nx
from networkx.exception import NetworkXNoCycle

import love_geometry.server.consts as consts
from love_geometry.server.services.validator import LoveStoryValidator


class CircleFinder:
    def find_circles_of_affection(self, love_story: list) -> Tuple[list, Optional[list]]:
        sentence_list = list()
        for sentence in love_story:
            sentence = sentence.get("data")

            sentence_graph_dict = self._build_sentence_dict(sentence)

            sentence_list.append(sentence_graph_dict)

        return self._find_cycles_in_sentences(sentence_list)

    @staticmethod
    def _build_sentence_dict(sentence: dict) -> Dict[nx.DiGraph]:
        sentence_dict = defaultdict(nx.DiGraph)

        for name, love_case in sentence.items():
            for feeling, persons in love_case.items():
                edges = list()
                for person in persons:
                    edge = name, person
                    edges.append(edge)

                sentence_dict[feeling].add_edges_from(edges, label=feeling)

        return sentence_dict

    def _find_cycles_in_sentences(self, sentence_list: list) -> Tuple[list, Optional[list]]:
        cycles_in_sentences = list()
        cheaters_list = list()
        for out_sentence in sentence_list:
            if consts.VALIDATE_LOVE_STORIES:
                cheaters = LoveStoryValidator.find_cheaters(out_sentence)
                cheaters_list.append(cheaters)
                if cheaters:
                    for cheater in cheaters:
                        remove_cheater_from_sentence = [graph.remove_node(cheater) for graph in out_sentence.values()]  # noqa F481

            output = self.__find_cycles(out_sentence)
            cycles_in_sentences.append(output)

        return cycles_in_sentences if not consts.VALIDATE_LOVE_STORIES else cycles_in_sentences, cheaters_list

    @staticmethod
    def __find_cycles(sentence: dict, visualize=consts.VISUALIZE_CIRCLES_OF_AFFECTION) -> dict:
        cycles = dict()
        for feeling, graph in sentence.items():
            try:
                cycles[feeling] = list(nx.find_cycle(graph))
            except NetworkXNoCycle:
                pass
            if visualize:
                color = random.choice(["red", "gray", "blue", "green", "yellow"])
                nx.draw(graph, with_labels=True, node_color=color)
        if visualize:
            plt.show()

        return cycles
