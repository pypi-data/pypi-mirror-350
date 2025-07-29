import copy


# TODO: move to python-sdk
class ServiceResponse:
    """
    A class to represent a service response.
    """

    def __init__(
        self,
        message_internal: dict,
        message_external: dict,
        is_success: bool = False,
        data: dict = None,
    ):
        """
        Initializes the ServiceResponse instance.

        :param status_code: HTTP status code of the response.
        :param message: Message describing the response.
        :param data: Optional data to be included in the response.
        """
        # self.status_code = status_code

        self.message = copy.deepcopy(message_internal)
        self.message_internal_english = message_internal
        # self.message_external_ml = {"en": message_external, "he": message_external}

        if isinstance(message_external, dict) and (
            "en" in message_external or "he" in message_external
        ):
            self.message_external_ml = message_external
        else:
            # Original behavior for string input
            self.message_external_ml = {"en": message_external, "he": message_external}

        self.is_success = is_success
        self.data = copy.deepcopy(data) if data else {}

    def to_http_response(self) -> dict:
        """
        Converts the ServiceResponse instance to a dictionary format suitable for HTTP response.

        :return: A dictionary representation of the ServiceResponse instance.
        """
        http_response = {
            # "statusCode": self.status_code,
            "message": self.message,
            "messageInternal": self.message_internal_english,
            "messageExternalMl": self.message_external_ml,
            "isSuccess": self.is_success,
            "data": self.data if self.data else {},
        }
        return http_response
