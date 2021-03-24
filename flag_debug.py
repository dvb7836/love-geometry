from pypeg2 import parse, List

from love_geometry.peg_parser.parser import LoveStory, Sentence


class ExtendedLoveStory(LoveStory):
    def __init__(self, *args, **kwargs):
        super(LoveStory, self).__init__(*args, **kwargs)

    def append(self, object) -> None:
        if object in self:
            raise
        super(ExtendedLoveStory, self).append(object) or list()


def main():
    love_story_text = "A loves C. A loves C."

    love_story = ExtendedLoveStory
    parsed_story = parse(love_story_text, love_story)
    return parsed_story


if __name__ == '__main__':
    print(main())
