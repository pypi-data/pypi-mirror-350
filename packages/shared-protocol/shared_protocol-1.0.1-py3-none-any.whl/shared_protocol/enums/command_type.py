from enum import Enum

class CommandType(str, Enum):
    REBOOT_DEVICE = "RebootDeviceCommand"
    CHECK_SIGNAL = "CheckSignalCommand"
    GET_MODULE_STATUS = "GetModuleStatusCommand"