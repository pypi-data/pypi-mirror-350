from enum import Enum

class EventType(str, Enum):
    DEVICE_REBOOTED = "DeviceRebootedEvent"
    SIGNAL_MEASURED = "SignalMeasuredEvent"