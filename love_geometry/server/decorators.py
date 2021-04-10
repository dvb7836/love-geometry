from functools import wraps
from http import HTTPStatus
from typing import Callable, Optional

from flask import g, jsonify, request
from werkzeug.exceptions import BadRequest


def expects_marshmallow_json(
    schema_class: Optional[Callable] = None,
    many: bool = False,
    force: bool = False
):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if (not force) and (not request.is_json):
                raise BadRequest("Not a JSON request")

            json_data = request.get_json(force=force)

            if json_data is None:
                raise BadRequest("Error decoding JSON object")

            try:
                schema = schema_class(many=many)
                decoding_result = schema.load(json_data)
            except Exception as e:
                raise BadRequest(f"Error decoding data according to schema: {e}")

            g.data = decoding_result
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def marshal_response_with(
    schema_class: Optional[Callable] = None,
    many: bool = False,
    envelope: str = None,
    status_code: int = HTTPStatus.OK
):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            func_result = f(*args, **kwargs)

            force_status_code = None
            if hasattr(func_result, "status_code"):
                force_status_code = func_result.status_code

            response_data = {"payload": [a.get("data") for a in func_result]}  # XXX
            response_code = status_code if force_status_code is None else force_status_code

            try:
                schema = schema_class(many=many)
                if not envelope:
                    encoding_result = schema.dump(response_data)
                else:
                    encoding_result = {
                        envelope: schema.dump(response_data)
                    }

                encoding_result = jsonify(encoding_result)
            except Exception as e:
                # TODO: add stack trace logging support
                error_message = str(e)
                raise BadRequest(
                    f"Error encoding data according to schema: {error_message}"
                )

            return encoding_result, response_code
        return decorated_function
    return decorator
