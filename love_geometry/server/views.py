import sys
import traceback
from logging import getLogger

from flask import Blueprint, g, jsonify

from love_geometry.server.exceptions import (BadRequestException, ParserError,
                                             ValidationError)
from love_geometry.server.services.orchestrator import LoveStoryOrchestrator
from love_geometry.server.services.serializer import (ApiResponseModelSchema,
                                                      InputModel, InputSchema)

from .decorators import expects_marshmallow_json, marshal_response_with

api_blueprint = Blueprint("api", __name__)
logger = getLogger(__name__)


@api_blueprint.route('/parse-love-story', methods=["POST"])
@expects_marshmallow_json(InputSchema)
@marshal_response_with(ApiResponseModelSchema)
def parse_love_story():
    parsed_request: InputModel = g.data

    orchestrator = LoveStoryOrchestrator(parsed_request.validate)

    return orchestrator.parse_love_story(parsed_request.love_story)


@api_blueprint.route('/find-circles-of-affection', methods=["POST"])
@expects_marshmallow_json(InputSchema)
@marshal_response_with(ApiResponseModelSchema, many=True, envelope="data")
def find_circles_of_affection():
    parsed_request: InputModel = g.data

    orchestrator = LoveStoryOrchestrator(parsed_request.validate)

    return orchestrator.find_circles_of_affection(parsed_request.love_story)


@api_blueprint.errorhandler(BadRequestException)
@api_blueprint.errorhandler(ParserError)
@api_blueprint.errorhandler(ValidationError)
def handle_api_exceptions(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code

    exc_type, exc_value, exc_traceback = sys.exc_info()
    stack_trace = traceback.format_exception(exc_type, exc_value, exc_traceback)

    logger.warning(
        f"{error.__class__.__name__} exception. Hidden payload: {error.hidden_payload} message: {error.message}"
    )

    stack_trace = "\n".join(stack_trace)
    logger.error(f"Stack trace: {stack_trace}")

    return response
