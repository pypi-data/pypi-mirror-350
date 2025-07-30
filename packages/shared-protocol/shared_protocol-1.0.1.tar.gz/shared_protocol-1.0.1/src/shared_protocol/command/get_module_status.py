from pydantic import BaseModel

from shared_protocol.command.base_command import BaseCommand


class GetModuleStatusCommand(BaseCommand,BaseModel):
    pass
