import time
from .events import Event, EventType, State
from .fsm import StateMachine
from .planner import GesturePlanner
from .mcu import MCUInterface
from .cloud import CloudClient
from .log import setup_logger

logger = setup_logger()

def run_main() -> None:
    fsm = StateMachine()
    planner = GesturePlanner()
    mcu = MCUInterface()
    cloud = CloudClient()

    # Enter initial state
    mcu.set_state(fsm.state.name)
    mcu.play_gesture(planner.on_enter_state(fsm.state))
