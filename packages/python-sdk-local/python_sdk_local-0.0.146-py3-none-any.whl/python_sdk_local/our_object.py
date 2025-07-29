import json
from abc import ABC, abstractmethod
# from logger_local.MetaLogger import ABCMetaLogger

from python_sdk_remote.mini_logger import MiniLogger as logger


# TODO Where are we using it? Shall we extend the usage of OurObject as the father of all our entities?
# TODO Why we removed the metaclass=ABCMetaLogger?
# class OurObject(ABC, metaclass=ABCMetaLogger):
class OurObject(ABC):
    def __init__(self, **kwargs):
        INIT_METHOD_NAME = '__init__'
        logger.start(INIT_METHOD_NAME, object={'kwargs': kwargs})
        self.kwargs = kwargs
        logger.end(INIT_METHOD_NAME, object={'kwargs': kwargs})

    @abstractmethod
    def get_name(self):
        """Returns the name of the object"""
        raise NotImplementedError(
            "Subclasses must implement the 'get_name' method.")

    def get(self, attr_name: str):
        """Returns the value of the attribute with the given name"""
        GET_METHOD_NAME = 'get'
        logger.start(GET_METHOD_NAME, object={'attr_name': attr_name})
        arguments = getattr(self, 'kwargs', None)
        value = arguments.get(attr_name, None)
        logger.end(GET_METHOD_NAME, object={'attr_name': attr_name})
        return value

    def get_all_arguments(self):
        """Returns all the arguments passed to the constructor as a dictionary"""
        return getattr(self, 'kwargs', None)

    def to_json(self) -> str:
        """Returns a json string representation of this object"""
        return json.dumps(self.__dict__)

    def from_json(self, json_string: str) -> 'OurObject':
        """Returns an instance of the class from a json string"""
        FROM_JSON_METHOD_NAME = 'from_json'
        logger.start(FROM_JSON_METHOD_NAME,
                     object={'json_string': json_string})
        self.__dict__ = json.loads(json_string)
        logger.end(FROM_JSON_METHOD_NAME,
                   object={'json_dict': self.__dict__})
        return self

    def __eq__(self, other) -> bool:
        """Checks if two objects are equal"""
        if not isinstance(other, OurObject):
            return False
        return self.__dict__ == other.__dict__

    def __ne__(self, other) -> bool:
        """Checks if two objects are not equal"""
        return not self.__eq__(other)
