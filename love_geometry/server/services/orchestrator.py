from love_geometry.server.services.parser import LoveStoryParser
from love_geometry.server.services.serializer import LoveStorySerializer
from love_geometry.server.services.circle_finder import CircleFinder


class LoveStoryOrchestrator:
    def __init__(self, validate_lovestory: bool):
        # TODO: use private / protected attributes
        self._validate_lovestory = validate_lovestory

        self.parser = LoveStoryParser(self._validate_lovestory)
        self.serializer = LoveStorySerializer()
        self.circle_finder = CircleFinder(self._validate_lovestory)

    def parse_love_story(self, love_story_text: str) -> list:
        parsed_love_story = self.parser.parse_love_story(love_story_text)

        return self.serializer.serialize(parsed_love_story)

    def find_circles_of_affection(self, love_story_text: str) -> dict:
        parsed_love_story = self.parser.parse_love_story(love_story_text)
        serialized_love_story = self.serializer.serialize(parsed_love_story)

        if self._validate_lovestory:
            circles_of_affection, cheaters = self.circle_finder.find_circles_of_affection(serialized_love_story)

            return {"circles_of_affection": circles_of_affection,
                    "cheaters": cheaters}

        return {"circles_of_affection": self.circle_finder.find_circles_of_affection(serialized_love_story),
                "cheaters": {}}
