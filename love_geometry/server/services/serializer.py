from marshmallow import Schema, fields, post_load
from dataclasses import dataclass
from http import HTTPStatus
from typing import Dict, List

from love_geometry.peg_parser.consts import FEELINGS


@dataclass
class InputModel(object):
    love_story: str = None
    validate: bool = None


class InputSchema(Schema):
    love_story = fields.Str(required=True)
    validate = fields.Bool(default=False)

    @post_load
    def make_instance(self, data, **_kwargs):
        return InputModel(**data)


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
    def serialize(parsed_love_story) -> Dict[str, list]:
        sentence_schema = SentenceSchema()
        sentences = sentence_schema.dump(parsed_love_story, many=True)

        return {"payload": [a.get("data") for a in sentences]}  # XXX


@dataclass
class ApiResponseModel(object):
    ok: bool = True
    message: str = None
    status_code: int = HTTPStatus.OK
    payload: List = None


class ApiResponseModelSchema(Schema):
    ok = fields.Boolean(required=True, allow_none=False)
    message = fields.Str(required=False, allow_none=True)
    status_code = fields.Int(required=True, allow_none=False)
    payload = fields.List(fields.Dict)
