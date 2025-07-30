from typing import  TypeVar

from shared_protocol.base_model import Base

T = TypeVar("T", bound="BaseCommand")


class BaseCommand(Base):
    device_code: str
    command_id: str

