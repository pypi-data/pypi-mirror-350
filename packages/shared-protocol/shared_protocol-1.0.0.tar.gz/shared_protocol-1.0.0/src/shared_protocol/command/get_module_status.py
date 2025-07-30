from pydantic import BaseModel

from src.shared_protocol.command.base_command import BaseCommand


class GetModuleStatusCommand(BaseCommand,BaseModel):
    pass
