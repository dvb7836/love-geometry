from __future__ import annotations
from marshmallow import Schema, fields

from love_geometry.peg_parser.consts import FEELINGS
from love_geometry.server.services.validator import LoveStoryValidator


LoveCase = type('LoveCase', (Schema, ), {
    attr: fields.List(fields.Str(required=True))
    for attr in FEELINGS
})


class SentenceSchema(Schema):
    data = fields.Dict(
        keys=fields.Str(required=True),
        values=fields.Nested(LoveCase(), required=True),
        many=True
    )
    errors = fields.List(fields.Str())


class LoveStorySerializer:
    @staticmethod
    def serialize(parsed_love_story) -> list:
        sentence_schema = SentenceSchema()
        sentences = list(sentence_schema.dump(parsed_love_story, many=True))  # already list
        if len(sentences) >= 2:
            LoveStoryValidator.check_for_duplicated_sentences(sentences)

        return sentences
