from datetime import datetime
from src.shared_protocol.event.base_event import BaseEvent


class NewMessageReceived(BaseEvent):
    id: int
    status: str
    from_: str
    datetime: datetime
    text: str
    module_id: str
    slot_number: int

