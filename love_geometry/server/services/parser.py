from __future__ import annotations
from pypeg2 import parse

from love_geometry.peg_parser.sentence import LoveStory, Sentence
from love_geometry.server.exceptions import ParserError

from pypeg2 import some


class LoveStoryParser(object):
    def __init__(self, validate_lovestory: bool):
        self.peg_parser = self._create_parser_class(validate_lovestory)

    def parse_love_story(self, love_story_text: str) -> LoveStory:
        try:
            parsed_story = parse(love_story_text, self.peg_parser)

        except SyntaxError as e:
            raise ParserError(e)

        return parsed_story

    def _create_parser_class(self, validate_lovestory):
        class ExtendedSentence(Sentence):
            VALIDATION_ENABLED = validate_lovestory

        class ExtendedLoveStory(LoveStory):
            grammar = some(ExtendedSentence)

        return ExtendedLoveStory
