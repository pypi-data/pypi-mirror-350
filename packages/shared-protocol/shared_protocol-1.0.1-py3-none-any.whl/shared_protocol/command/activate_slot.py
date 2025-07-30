from shared_protocol.command.base_command import BaseCommand


class ActivateSlotCommand(BaseCommand):
    module_id: str
    slot_number: int
    force: bool = False
