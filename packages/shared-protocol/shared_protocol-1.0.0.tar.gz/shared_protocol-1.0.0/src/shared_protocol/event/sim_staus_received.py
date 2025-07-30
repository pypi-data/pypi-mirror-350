from src.shared_protocol.event.base_event import BaseEvent


class SimStatusReceived(BaseEvent):
    signal_quality: int | None = None
    network_status: int | None = None
    module_id: str
    ccid: str | None = None
    cimi: str | None = None
    carrier: str | None = None
    network: str | None = None
    number: str | None = None
    slot_number: int | None = None
