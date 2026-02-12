from dataclasses import dataclass
from typing import Optional
from log import setup_logger

logger = setup_logger()


@dataclass
class McuCommand:
    cmd: str
    state: Optional[str] = None
    gesture: Optional[str] = None


class MCUInterface:
    """Stub for now; later this will speak UART to the ESP32."""

    def set_state(self, state_name: str) -> None:
        # logger.info(f"MCU set_state: {state_name}")
        pass

    def play_gesture(self, gesture_id: str) -> None:
        # logger.info(f"MCU play_gesture: {gesture_id}")
        pass
