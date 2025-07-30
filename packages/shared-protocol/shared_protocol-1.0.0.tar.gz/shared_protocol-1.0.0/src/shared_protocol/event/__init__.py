from src.shared_protocol.event.change_reported import ChangeReported
from src.shared_protocol.event.module_initialized import ModuleInitialized
from src.shared_protocol.event.module_status_received import ModuleStatusReceived
from src.shared_protocol.event.new_message_received import NewMessageReceived
from src.shared_protocol.event.sim_staus_received import SimStatusReceived

event_cls = {
    ModuleStatusReceived.type(): ModuleStatusReceived,
    SimStatusReceived.type(): SimStatusReceived,
    ChangeReported.type(): ChangeReported,
    ModuleInitialized.type(): ModuleInitialized,
    NewMessageReceived.type(): NewMessageReceived,
}
