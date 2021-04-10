from __future__ import annotations
from pypeg2 import parse

from love_geometry.peg_parser.sentence import LoveStory
from love_geometry.server.exceptions import ParserError


class LoveStoryParser(object):
    @staticmethod
    def parse_love_story(love_story_text: str) -> LoveStory:
        try:
            parsed_story = parse(love_story_text, LoveStory)
        except SyntaxError as e:
            raise ParserError(exception=e)

        return parsed_story
