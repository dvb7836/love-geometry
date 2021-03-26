from .circle_finder import CircleFinder
from .parser import LoveStoryParser
from .serializer import LoveStorySerializer
from .validator import LoveStoryValidator


class LoveStoryOrchestrator:
    def __init__(self, validate_love_story: bool):
        self._validate_love_story = validate_love_story

        self._parser = LoveStoryParser()
        self._validator = LoveStoryValidator()
        self._serializer = LoveStorySerializer()
        self._circle_finder = CircleFinder(self._validate_love_story)

    def parse_love_story(self, love_story_text: str) -> list:
        parsed_love_story = self._parser.parse_love_story(love_story_text)
        if self._validate_love_story:
            self._validator.validate(parsed_love_story)

        return self._serializer.serialize(parsed_love_story)

    def find_circles_of_affection(self, love_story_text: str) -> dict:
        parsed_love_story = self._parser.parse_love_story(love_story_text)
        serialized_love_story = self._serializer.serialize(parsed_love_story)

        if self._validate_love_story:
            circles_of_affection, cheaters = self._circle_finder.find_circles_of_affection(serialized_love_story)

            return {"circles_of_affection": circles_of_affection,
                    "cheaters": cheaters}

        return {"circles_of_affection": self._circle_finder.find_circles_of_affection(serialized_love_story),
                "cheaters": {}}
