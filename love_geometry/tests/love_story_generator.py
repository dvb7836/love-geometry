from typing import Set, Tuple
import uuid
import random
import string

from love_geometry.peg_parser.consts import FEELINGS, DOUBLE_ENDED_RELATIONSHIP_FLAG_KEYWORD, LOVE_CASE_SEPARATORS, \
    SENTENCE_SEPARATOR


def generate_love_story(n=10, de_flag=False) -> Tuple[str, Set]:
    sentences, names = list(zip(*[_generate_love_story_sentence(de_flag) for _ in range(n)]))

    story = "\n".join(sentences)
    names = set.union(*names)

    return story, names


def _generate_love_story_sentence(de_flag=False) -> Tuple[str, Set]:
    first_persons = {str(uuid.uuid4()).split("-")[0] for _ in range(len(LOVE_CASE_SEPARATORS) * len(FEELINGS))}
    first_persons_copy = first_persons.copy()

    random.shuffle(LOVE_CASE_SEPARATORS)
    not_last_case = (lambda i, j: i + j != (len(FEELINGS) + len(LOVE_CASE_SEPARATORS) - 1)) if not de_flag else \
        (lambda i, j: True)
    love_case = (
        lambda feeling, separator, i, j: (
            first_persons.pop(), feeling, random.choice(string.ascii_lowercase), separator if not_last_case(i, j) else "")
    )
    sentence_text = " ".join(
        [
            " ".join(love_case(feeling, separator, i, j))
            for i, feeling in enumerate(FEELINGS)
            for j, separator in (enumerate(LOVE_CASE_SEPARATORS) if not de_flag else enumerate(LOVE_CASE_SEPARATORS[:1]))
        ]
    ).replace(" ,", ",").rstrip() + SENTENCE_SEPARATOR
    if de_flag:
        for feeling in FEELINGS:
            sentence_text = sentence_text.replace(feeling, f"{DOUBLE_ENDED_RELATIONSHIP_FLAG_KEYWORD} {feeling}", 1)

    return sentence_text, first_persons_copy
