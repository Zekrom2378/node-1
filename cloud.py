import os
from dataclasses import dataclass

from google import genai


@dataclass
class LlmResult:
    response_text: str


class CloudClient:
    """
    Gemini-backed CloudClient.
    Keeps the same interface as the earlier stub:
      - CloudClient.run(prompt_text: str) -> LlmResult
    """

    def __init__(self, model: str = "gemini-1.5-flash") -> None:
        # The google-genai SDK will automatically read GEMINI_API_KEY or GOOGLE_API_KEY.
        # We'll still sanity-check so failures are obvious.
        if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
            raise RuntimeError(
                "Gemini API key not set. Put GEMINI_API_KEY (recommended) in your .env "
                "and call load_dotenv() in main.py."
            )

        self.client = genai.Client()  # key taken from env by default :contentReference[oaicite:4]{index=4}
        self.model = model

        # System instruction to enforce NODE-1's concise “2 sentences max + offer details” behavior.
        self.system_instruction = (
            "You are a concise assistant. Answer in 1–2 sentences. "
            "If and only if more explanation is needed, give a short summary and ask if the user wants details."
        )

    def run(self, prompt_text: str) -> LlmResult:
        prompt_text = (prompt_text or "").strip()
        if not prompt_text:
            return LlmResult(response_text="No prompt provided.")

        # Gemini SDK: generate_content with system instruction + user prompt. :contentReference[oaicite:5]{index=5}
        resp = self.client.models.generate_content(
            model=self.model,
            contents=prompt_text,
            config={
                "system_instruction": self.system_instruction,
                # Optional knobs you can tune later:
                # "temperature": 0.3,
                # "max_output_tokens": 200,
            },
        )

        # The SDK typically exposes generated text as resp.text.
        text = (getattr(resp, "text", "") or "").strip()
        if not text:
            text = "No response text received."

        return LlmResult(response_text=text)