import traceback
from functools import wraps
from http import HTTPStatus
from typing import Any
# TODO: use logger_local everywhere with meta loggers & remove logger start/end
from python_sdk_remote.mini_logger import MiniLogger as logger
from user_context_remote.user_context import UserContext

from .utilities import camel_to_snake, snake_to_camel, to_dict, to_json

HEADERS_KEY = 'headers'
AUTHORIZATION_KEY = 'Authorization'
AUTHORIZATION_PREFIX = 'Bearer '


# TODO Align those methods with typescript-sdk https://github.com/circles-zone/typescript-sdk-remote-typescript-package/blob/dev/typescript-sdk/src/utils/index.ts  # noqa
# TODO Shall we create also createInternalServerErrorHttpResponse(), createOkHttpResponse() like we have in TypeScript?

def get_payload_dict_from_event(event: dict) -> dict:
    """Extracts params sent with payload"""
    return to_dict(event.get('body'))  # TODO all `return statement` should be `return variable`


def get_path_parameters_dict_from_event(event: dict) -> dict:
    """Extracts params sent implicitly: `url/param?test=5` -> param
    (when the path is defined with /{param})"""
    return event.get('pathParameters') or {}


def get_query_string_parameters_from_event(event: dict) -> dict:
    """Extracts params sent explicitly: `url/test?a=1&b=2` ->  {'a': '1', 'b': '2'}"""
    return event.get("queryStringParameters") or {}  # params sent with ?a=1&b=2


def get_request_parameters_from_event(event: dict) -> dict:
    """Extracts all params from the event object.
    The order of precedence is: payload > path > query string
    returns a dictionary with all the parameters, with both camelCase and snake_case keys."""
    all_parameters_dict = get_payload_dict_from_event(event)
    all_parameters_dict.update(get_path_parameters_dict_from_event(event))
    all_parameters_dict.update(get_query_string_parameters_from_event(event))
    all_parameters_dict = {camel_to_snake(key): value for key, value in all_parameters_dict.items()}
    all_parameters_dict.update({snake_to_camel(key): value for key, value in all_parameters_dict.items()})
    return all_parameters_dict


# TODO: move everything related to serverless to another file
# TODO: test
# TODO Do we use is_validate_user_jwt? Where? Is it mandatory/neede?
def handler_decorator(logger, is_validate_user_jwt: bool = True):
    """Decorator for AWS Lambda handler functions. It wraps the handler function with logging and error handling.
    Usage:
    from python_sdk_local.http_response import handler_decorator
    logger = ...
    @handler_decorator(logger=logger)
    def my_handler(request_parameters: dict) -> dict:
        return {"message": "Hello, World!"}"""

    def decorator(handler: callable) -> callable:
        @wraps(handler)
        def wrapper(event, context):
            handler_response = None
            try:
                logger.start(object={"event": event, "context": context})
                request_parameters = get_request_parameters_from_event(event)

                if is_validate_user_jwt:
                    user_jwt = get_user_jwt_from_event(event)
                    if user_jwt:
                        request_parameters["user_context"] = UserContext.login_using_user_jwt(user_jwt)
                    else:
                        logger.warning("No user_jwt provided")
                body_result = handler(request_parameters)
                handler_response = create_ok_http_response(body_result)
            except Exception as e:
                handler_response = create_error_http_response(e)
            finally:
                logger.end(object={"handler_response": handler_response})
            return handler_response

        return wrapper

    return decorator


# TODO: should we auto detect user_jwt if not provided?
def create_authorization_http_headers(user_jwt: str) -> dict:
    logger.start(object={"user_jwt": user_jwt})
    authorization_http_headers = {
        'Content-Type': 'application/json',
        'Authorization': AUTHORIZATION_PREFIX + user_jwt,
    }
    logger.end(object={"authorization_http_headers": authorization_http_headers})
    return authorization_http_headers


def get_user_jwt_from_event(event: dict) -> str:
    logger.start(object={"event": event})
    auth_header = event.get(HEADERS_KEY, {}).get(AUTHORIZATION_KEY, "")
    if auth_header is None:
        auth_header = event.get(HEADERS_KEY, {}).get(AUTHORIZATION_KEY.lower(), "")
    user_jwt = auth_header.split(AUTHORIZATION_PREFIX)[-1]
    logger.end(object={"user_jwt": user_jwt})
    return user_jwt


def create_return_http_headers() -> dict:
    logger.start()
    return_http_headers = {
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
    }
    logger.end(object={"return_http_headers": return_http_headers})
    return return_http_headers


def create_error_http_response(exception: Exception, status_code: HTTPStatus = HTTPStatus.BAD_REQUEST) -> dict:
    logger.start(object={"exception": exception})
    error_http_response = {
        "statusCode": status_code.value,
        "headers": create_return_http_headers(),
        "body": create_http_body({"error": str(exception),
                                  "traceback": traceback.format_exc()}),
    }
    logger.end(object={"error_http_response": error_http_response})
    return error_http_response


def create_ok_http_response(body: Any) -> dict:
    logger.start(object={"body": body})
    # TODO: test sending statusCode/headers/body inside the body
    if isinstance(body, str) and body.startswith("{") and body.endswith("}"):
        body = to_dict(body)
    if isinstance(body, dict):
        status_code = body.get("statusCode")
        headers = body.get("headers")
        body_result = body.get("body")
    else:
        status_code = headers = body_result = None
    ok_http_response = {
        "statusCode": status_code or HTTPStatus.OK.value,
        "headers": headers or create_return_http_headers(),
        "body": create_http_body(body_result or body)
    }
    logger.end(object={"ok_http_response": ok_http_response})
    return ok_http_response


# https://google.github.io/styleguide/jsoncstyleguide.xml?showone=Property_Name_Format#Property_Name_Format
def create_http_body(body: Any) -> str:
    # TODO console.warning() if the body is not a valid camelCase JSON
    # https://stackoverflow.com/questions/17156078/converting-identifier-naming-between-camelcase-and-underscores-during-json-seria
    logger.start(object={"body": body})
    http_body = to_json(body)
    logger.end(object={"http_body": http_body})
    return http_body
