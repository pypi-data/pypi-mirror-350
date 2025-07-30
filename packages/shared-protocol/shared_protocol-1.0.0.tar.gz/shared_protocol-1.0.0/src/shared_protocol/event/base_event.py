from src.shared_protocol.base_model import Base


class BaseEvent(Base):
    device_code: str
    event_id: str
    command_id: str | None = None
