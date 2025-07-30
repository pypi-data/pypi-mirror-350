from datetime import datetime

from pydantic import BaseModel

from shared_protocol.event.base_event import BaseEvent


class SimCard(BaseModel):
    id: int
    cimi: str | None
    ccid: str | None
    carrier: str | None
    network: str | None
    registered: bool | None
    number: str | None
    created_at: datetime


class Module(BaseModel):
    id: int
    imei: str
    created_at: datetime
    port: str
    name: str
    slot_count: int
    type: str
    first_slot_number: int
    driver: str
    baudrate: int



class ModuleSimCard(BaseModel):
    id: int
    module_id: int
    sim_card_id: int
    slot_number: int
    created_at: datetime


class ChangeReported(BaseEvent):
    sim_cards: list[SimCard]
    modules: list[Module]
    module_sim_cards: list[ModuleSimCard]
