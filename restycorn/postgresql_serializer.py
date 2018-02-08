from .base_serializer import BaseSerializer
from .exceptions import SerializationError


class PostgreSQLSerializer(BaseSerializer):
    def __init__(self, fields):
        self.fields = fields

    def serialize(self, item) -> dict:
        result = {}
        for key, val in item.items():
            if key in self.fields:
                result[key] = val

        if len(result) != len(self.fields):
            raise SerializationError()

        return result
