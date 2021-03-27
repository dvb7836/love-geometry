from distutils.util import strtobool
from flask import Blueprint, request, abort
import json
from http import HTTPStatus
from marshmallow import ValidationError as MarshmallowValidationError

from love_geometry.server.exceptions import ParserError, ValidationError
from love_geometry.server.services.orchestrator import LoveStoryOrchestrator

from .services.serializer import InputSchema
from .util import str_to_bool


api_blueprint = Blueprint("api", __name__)


@api_blueprint.route('/parse-love-story', methods=["POST"])
def parse_love_story():
    love_story = request.json.get("love_story")
    validate = str_to_bool(request.json.get("validate"))
    try:
        InputSchema().load({"love_story": love_story, "validate": validate})
    except MarshmallowValidationError as err:
        return abort(HTTPStatus.NOT_ACCEPTABLE, f"{err}")

    orchestrator = LoveStoryOrchestrator(validate)
    try:
        result = orchestrator.parse_love_story(love_story)

    except ParserError as e:
        err = {"message": f"Can't parse provided Love Story: `{e}`"}
        return abort(HTTPStatus.UNPROCESSABLE_ENTITY, err)
    except ValidationError as e:
        return abort(HTTPStatus.NOT_ACCEPTABLE, e)

    return json.dumps(result)


@api_blueprint.route('/find-circles-of-affection', methods=["POST"])
def find_circles_of_affection():
    love_story = request.json.get("love_story")
    validate = str_to_bool(request.json.get("validate"))
    try:
        InputSchema().load({"love_story": love_story, "validate": validate})
    except MarshmallowValidationError as err:
        return abort(HTTPStatus.NOT_ACCEPTABLE, f"{err}")

    orchestrator = LoveStoryOrchestrator(validate)
    try:
        result = orchestrator.find_circles_of_affection(love_story)

    except ParserError as e:
        err = {"message": f"Can't parse provided Love Story: `{e}`"}
        return abort(HTTPStatus.UNPROCESSABLE_ENTITY, err)
    except ValidationError as e:
        return abort(HTTPStatus.NOT_ACCEPTABLE, e)

    return json.dumps(result)
