from pydantic import BaseModel
from uuid import UUID

from shared_protocol.command.base_command import BaseCommand


class DeviceRebootedAck(BaseCommand, BaseModel):
    command_id: UUID
    module_id: int
    success: bool