from love_geometry.server.services.serializer import ApiResponseModel, ApiResponseModelSchema
import json
from http import HTTPStatus


class ProjectBaseException(Exception):
    def __init__(self, message, status_code=None, payload=None, hidden_payload=None):
        super().__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload
        self.hidden_payload = hidden_payload

    def to_dict(self):
        resp = ApiResponseModel(ok=False, message=self.message, status_code=self.status_code)
        if self.payload:
            resp.payload = self.payload

        return ApiResponseModelSchema().dump(resp)

    def __repr__(self):
        text = self.to_dict()
        return json.dumps(text, indent=4, sort_keys=True)

    def __str__(self):
        return self.__repr__()


class ParserError(ProjectBaseException):
    def __init__(self, message="Can't parse provided Love Story.", payload=None, exception=None):
        super().__init__(message=message, status_code=HTTPStatus.UNPROCESSABLE_ENTITY, payload=payload)

        self.hidden_payload = {
            "exception": str(exception)
        }


class ValidationError(ProjectBaseException):
    def __init__(self, message=None, payload=None, exception=None):
        super().__init__(message=message, status_code=HTTPStatus.NOT_ACCEPTABLE, payload=payload)

        self.hidden_payload = {
            "exception": str(exception)
        }


class BadRequestException(ProjectBaseException):
    def __init__(self, message="Bad Request", payload=None, exception=None):
        super().__init__(message=message, status_code=HTTPStatus.BAD_REQUEST, payload=payload)

        self.hidden_payload = {
            "exception": str(exception)
        }
