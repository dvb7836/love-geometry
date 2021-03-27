from collections import OrderedDict

from love_geometry.server.services.parser import LoveStoryParser
from love_geometry.server.exceptions import ValidationError
from love_geometry.server.services.orchestrator import LoveStoryOrchestrator
from love_geometry.peg_parser.consts import FEELINGS, LOVE_CASE_SEPARATORS
from love_geometry.tests.love_story_generator import generate_love_story

import pytest


def test_should_parse_single_sentence_story():
    love_story_sentence, first_person_names = generate_love_story(1)

    love_story = LoveStoryParser().parse_love_story(love_story_sentence)

    assert isinstance(love_story, list)
    contains_only_one_sentence = len(love_story) == 1
    assert contains_only_one_sentence
    expected_sentence_length = (len(love_story[0]) == len(LOVE_CASE_SEPARATORS) * len(FEELINGS))
    expected_sentence_length = expected_sentence_length
    assert expected_sentence_length
    for name in first_person_names:
        assert name in love_story[0]
        assert isinstance(love_story[0][name].data, OrderedDict)
        has_feelings = any([(str(f) == feeling) for feeling in FEELINGS for f in love_story[0][name].data])
        assert has_feelings
        name_is_string = any([
            (love_story[0][name].data.get(feeling)) and isinstance(love_story[0][name].data.get(feeling)[0], str)
            for feeling in FEELINGS
        ])
        assert name_is_string


def test_should_parse_multiple_sentence_story():
    sentences_count = 100
    love_story_text, first_person_names = generate_love_story(sentences_count)

    love_story = LoveStoryParser().parse_love_story(love_story_text)

    assert isinstance(love_story, list)
    expected_story_length = len(love_story) == sentences_count
    assert expected_story_length

    expected_sentence_length = all(len(sentence) == len(LOVE_CASE_SEPARATORS)*len(FEELINGS) for sentence in love_story)
    assert expected_sentence_length


def test_should_parse_story_with_flag_keyword():
    love_story_sentence, first_person_names = "A mutually loves B and C mutually hates D.", ["A", "B", "C", "D"]
    feelings = ["loves", "hates"]
    love_story = LoveStoryParser().parse_love_story(love_story_sentence)
    assert isinstance(love_story, list)

    contains_only_one_sentence = len(love_story) == 1
    assert contains_only_one_sentence
    assert len(love_story[0]) == 4
    assert all(name in love_story[0] for name in first_person_names)
    for f in feelings:
        p1, p2 = first_person_names.pop(0), first_person_names.pop(0)
        assert love_story[0][p1][f][0] == p2
        assert love_story[0][p2][f][0] == p1


def test_should_error_if_duplicated_love_case_and_validation_on():
    love_story_sentence = "A loves A."

    with pytest.raises(ValidationError) as excinfo:
        LoveStoryOrchestrator(validate_love_story=True).parse_love_story(love_story_sentence)

    assert excinfo.value.args[0] == "feelings to itself are not permitted"


def test_should_not_error_if_duplicated_love_case():
    love_story_sentence = "A loves A."

    assert LoveStoryOrchestrator(validate_love_story=False).parse_love_story(love_story_sentence)


def test_should_error_if_multiple_feelings_to_one_person_and_validation_on():
    love_story_sentence = "A loves B and A hates B."

    with pytest.raises(ValidationError) as excinfo:
        LoveStoryOrchestrator(validate_love_story=True).parse_love_story(love_story_sentence)

    assert excinfo.value.args[0] == "duplicated relationship: A - ['B']"


def test_should_not_error_if_multiple_feelings_to_one_person():
    love_story_sentence = "A loves B and A hates B."

    assert LoveStoryOrchestrator(validate_love_story=False).parse_love_story(love_story_sentence)


def test_should_error_if_duplicated_sentence_and_validation_on():
    love_story_sentence = "A loves B. A loves B."

    with pytest.raises(ValidationError) as excinfo:
        LoveStoryOrchestrator(validate_love_story=True).parse_love_story(love_story_sentence)

    assert excinfo.value.args[0] == "duplicated sentences"


def test_should_not_error_if_duplicated_sentence():
    love_story_sentence = "A loves B. A loves B."

    assert LoveStoryOrchestrator(validate_love_story=False).parse_love_story(love_story_sentence)
