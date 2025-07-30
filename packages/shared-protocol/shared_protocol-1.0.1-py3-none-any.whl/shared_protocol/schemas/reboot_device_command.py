from pydantic import BaseModel
from uuid import UUID

from shared_protocol.command.base_command import BaseCommand


class RebootDeviceCommand(BaseCommand, BaseModel):
    device_id: UUID
    module_id: int
    force: bool = True