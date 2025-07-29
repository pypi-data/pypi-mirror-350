import datetime
import json
from abc import ABC, abstractmethod
from dateutil import parser
import xml.etree.ElementTree as ET

from requests import Response


class Serializer(ABC):
    @abstractmethod
    def get_content_type(self):
        raise NotImplementedError()

    @abstractmethod
    def serialize(self, data):
        raise NotImplementedError()

    @abstractmethod
    def deserialize(self, response: Response):
        raise NotImplementedError()


class NoSerializer(Serializer):
    def get_content_type(self):
        return "application/octet-stream"

    def serialize(self, data):
        return data

    def deserialize(self, response: Response):
        return response


class TextSerializer(Serializer):
    def get_content_type(self):
        return "text/plain"

    def serialize(self, data):
        return str(data)

    def deserialize(self, response: Response):
        return str(response.text)


class JsonSerializer(Serializer):
    def get_content_type(self):
        return "application/json"

    def serialize(self, data):
        def datetime_handler(obj):
            if isinstance(obj, datetime.datetime):
                return obj.isoformat()
            raise TypeError("Type not serializable")

        return json.dumps(data, default=datetime_handler)

    def deserialize(self, response: Response):
        return json.loads(response.text)


class XmlSerializer(Serializer):
    def get_content_type(self):
        return "application/xml"

    def serialize(self, data, tag: str = "Object") -> str:
        elem: ET.Element = self._dict_to_xml(tag, data)
        return ET.tostring(elem).decode()

    def deserialize(self, response: Response):
        pass

    def _dict_to_xml(self, tag, d):
        elem = ET.Element(tag)
        for key, val in d.items():
            if isinstance(val, dict):
                child = self._dict_to_xml(key, val)
            else:
                child = ET.Element(key)
                child.text = str(val)
            elem.append(child)
        return elem
# def json_serializer_with_datetime(data):
#     def datetime_handler(obj):
#         if isinstance(obj, datetime.datetime):
#             return obj.isoformat()
#         raise TypeError("Type not serializable")
#
#     return json.dumps(data, default=datetime_handler)
#
#
# # JSON Deserializer with datetime support
# def json_deserializer_with_datetime(json_str):
#     def datetime_parser(dct):
#         for k, v in dct.items():
#             if isinstance(v, str):
#                 try:
#                     dct[k] = parser.parse(v)
#                 except:
#                     pass
#         return dct
#
#     return json.loads(json_str, object_hook=datetime_parser)