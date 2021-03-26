import json
from flask import Blueprint, request, abort

from love_geometry.server.exceptions import ParserError, ValidationError
from love_geometry.server.services.orchestrator import LoveStoryOrchestrator

api_blueprint = Blueprint("api", __name__)


def str_to_bool(value):
    if value is None:
        return False

    if isinstance(value, bool):
        return value

    value = str(value).strip()
    if not value:
        return False

    ret = bool(value)
    if not ret:
        return False

    value = str(value).lower()
    ret = True if value in ["true", "1", "on", "yes"] else False

    return ret


@api_blueprint.route('/parse-love-story', methods=["POST"])
def parse_love_story():
    love_story = request.json.get("love_story")
    validate = str_to_bool(request.json.get("validate"))
    if not isinstance(love_story, str):
        return abort(422, "incorrect input")

    orchestrator = LoveStoryOrchestrator(validate)
    try:
        result = orchestrator.parse_love_story(love_story)

    except ParserError as e:
        err = {"message": f"Can't parse provided Love Story: `{e}`"}
        return abort(422, err)
    except ValidationError as e:
        return abort(422, e)

    return json.dumps(result)


@api_blueprint.route('/find-circles-of-affection', methods=["POST"])
def find_circles_of_affection():
    love_story = request.json.get("love_story")

    orchestrator = LoveStoryOrchestrator()
    try:
        result = orchestrator.find_circles_of_affection(love_story)

    except ParserError as e:
        err = {"message": f"Can't parse provided Love Story: `{e}`"}
        return abort(422, err)
    except ValidationError as e:
        return abort(422, e)

    return json.dumps(result)
