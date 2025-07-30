from enum import Enum

class AckType(str, Enum):
    DEVICE_REBOOTED = "DeviceRebootedAck"
    SIGNAL_RESPONSE = "SignalStrengthAck"