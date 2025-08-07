from bson import ObjectId
from pydantic_core import CoreSchema, PydanticCustomError, core_schema
from typing import Any

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler) -> CoreSchema:
        def validate_from_str(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise PydanticCustomError('invalid_object_id', 'Invalid ObjectId')
            return ObjectId(value)

        return core_schema.union_schema(
            [
                core_schema.is_instance_schema(ObjectId),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )


def get_object_id(id: str):
    return PyObjectId(id)