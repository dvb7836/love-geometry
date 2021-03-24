from __future__ import annotations
from pypeg2 import parse

from love_geometry.peg_parser.sentence import LoveStory
from love_geometry.server.exceptions import ParserError


class LoveStoryParser:
    def __init__(self):
        self.peg_parser = LoveStory

    def parse_love_story(self, love_story_text: str) -> LoveStory:
        try:
            parsed_story = parse(love_story_text, self.peg_parser)

        except SyntaxError as e:
            raise ParserError(e)

        return parsed_story
