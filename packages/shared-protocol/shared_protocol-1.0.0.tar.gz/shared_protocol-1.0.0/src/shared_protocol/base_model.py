from typing import TypeVar, Type
from uuid import UUID

from pydantic import BaseModel

T = TypeVar("T", bound="BaseCommand")


class Base(BaseModel):
    @classmethod
    def type(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def from_json(cls: Type[T], data: dict) -> T:
        valid_keys = cls.__annotations__.keys()
        filtered_data = {k: v for k, v in data.items() if
                         k in list(valid_keys) + ["device_code", "command_id" , "event_id"]}
        return cls(**filtered_data)

    def to_dict(self):
        def serialize(value):
            if isinstance(value, UUID):
                return str(value)
            if isinstance(value, BaseModel):
                return value.dict()
            if isinstance(value, list):
                return [serialize(item) for item in value]
            if hasattr(value, "__dict__"):
                return {
                    k: serialize(v) for k, v in value.__dict__.items()
                    if not k.startswith("_")  # حذف ویژگی‌های خصوصی
                }
            return value

        return {k: serialize(v) for k, v in self.__dict__.items()}

    @classmethod
    def name(cls):
        return cls.__name__
