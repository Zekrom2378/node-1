import time
from dataclasses import dataclass
from events import State, Event, EventType
from config import ATTENTIVE_TIMEOUT_S, LISTENING_TIMEOUT_S, THINKING_TIMEOUT_S
from log import setup_logger

logger = setup_logger()


@dataclass
class Context:
    last_state_ts: float
    prompt_text: str = ""
    response_text: str = ""


class StateMachine:
    def __init__(self) -> None:
        self.state = State.IDLE
        self.ctx = Context(last_state_ts=time.monotonic())

    def enter(self, new_state: State) -> None:
        self.state = new_state
        self.ctx.last_state_ts = time.monotonic()
        logger.info(f"\n[!] STATE CHANGE: {self.state.name}")

    def timed_out(self) -> bool:
        dt = time.monotonic() - self.ctx.last_state_ts
        if self.state == State.ATTENTIVE:
            return dt > ATTENTIVE_TIMEOUT_S
        if self.state == State.LISTENING:
            return dt > LISTENING_TIMEOUT_S
        if self.state == State.THINKING:
            return dt > THINKING_TIMEOUT_S
        return False

    def handle(self, ev: Event) -> None:
        s = self.state
        if ev.type == EventType.ERROR:
            self.enter(State.ERROR)
            return

        # Extract text if available for logic checks
        input_text = (ev.data or {}).get("text", "").lower()
        wake_word = "node"  # Define your wake word here

        if s == State.IDLE:
            if ev.type == EventType.HEARD_SPEECH:
                if wake_word in input_text:
                    self.ctx.prompt_text = input_text.replace(wake_word, "").strip()
                    # Jump transition: If prompt followed the wake word immediately
                    if self.ctx.prompt_text:
                        self.enter(State.THINKING)
                    else:
                        self.enter(State.LISTENING)
                else:
                    self.enter(State.ATTENTIVE)

        elif s == State.ATTENTIVE:
            if ev.type == EventType.WAKE_WORD:
                self.enter(State.LISTENING)
            elif ev.type == EventType.TIMEOUT:
                self.enter(State.IDLE)

        elif s == State.LISTENING:
            if ev.type == EventType.PROMPT_TEXT and ev.data:
                self.ctx.prompt_text = input_text
                self.enter(State.THINKING)
            elif ev.type == EventType.TIMEOUT:
                self.enter(State.IDLE)

        elif s == State.THINKING:
            if ev.type == EventType.LLM_RESULT and ev.data:
                pass
                # response state chosen externally by planner
            elif ev.type == EventType.TIMEOUT:
                self.enter(State.ERROR)

        elif s in (State.RESPOND_SHORT, State.RESPOND_MED, State.RESPOND_LONG):
            if ev.type == EventType.RESET:
                self.enter(State.IDLE)

        elif s == State.ERROR:
            if ev.type == EventType.RESET:
                self.enter(State.IDLE)
