import time
from dataclasses import dataclass


@dataclass
class LlmResult:
    response_text: str


class CloudClient:
    """Stub: replace with ASR/LLM calls later."""

    def run(self, prompt_text: str) -> LlmResult:
        # Simulate variable latency
        time.sleep(1.0)
        # Fake response
        return LlmResult(response_text=f"Understood. You said: {prompt_text}")
