from dataclasses import dataclass
from .events import State
from .config import SHORT_MAX, MED_MAX


@dataclass
class Plan:
    state_after: State
    gesture_id: str


class GesturePlanner:
    """Maps states/response length to gesture IDs (non-emotional)."""

    def on_enter_state(self, state: State) -> str:
        return {
            State.IDLE: "idle_breathe",
            State.ATTENTIVE: "attend_pose",
            State.LISTENING: "listen_pose",
            State.THINKING: "thinking_sway",
            State.ERROR: "error_pose",
        }.get(state, "neutral")

    def plan_response(self, response_text: str) -> Plan:
        n = len(response_text)
        if n <= SHORT_MAX:
            return Plan(State.RESPOND_SHORT, "deliver_short")
        if n <= MED_MAX:
            return Plan(State.RESPOND_MED, "deliver_med")
        return Plan(State.RESPOND_LONG, "deliver_long")
