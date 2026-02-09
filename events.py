from dataclasses import dataclass
from enum import Enum, auto
from typing import Optional


class State(Enum):
    IDLE = auto()
    ATTENTIVE = auto()
    LISTENING = auto()
    THINKING = auto()
    RESPOND_SHORT = auto()
    RESPOND_MED = auto()
    RESPOND_LONG = auto()
    ERROR = auto()


class EventType(Enum):
    HEARD_SPEECH = auto()
    WAKE_WORD = auto()
    PROMPT_TEXT = auto()
    LLM_RESULT = auto()
    TIMEOUT = auto()
    ERROR = auto()
    RESET = auto()


@dataclass
class Event:
    type: EventType
    data: Optional[dict] = None
