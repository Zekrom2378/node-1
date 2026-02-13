import os
from dataclasses import dataclass
from dotenv import load_dotenv
from google import genai
load_dotenv()


def ListModels():
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
    for model in client.models.list():
        print(model.name)


@dataclass
class LlmResult:
    response_text: str


class CloudClient:
    """
    Gemini-backed CloudClient.
    Keeps the same interface as the earlier stub:
      - CloudClient.run(prompt_text: str) -> LlmResult
    """

    def __init__(self, model: str = "gemini-2.5-flash") -> None:
        # The google-genai SDK will automatically read GEMINI_API_KEY or GOOGLE_API_KEY.
        # If gemini-1.5-flash fails, try "gemini-2.0-flash-exp" or "gemini-1.5-flash-latest"
        if not (os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")):
            raise RuntimeError(
                "Gemini API key not set. Put GEMINI_API_KEY in your .env"
            )

        self.client = genai.Client()  # key taken from env by default :contentReference[oaicite:4]{index=4}
        self.model = model

        # System instruction to enforce NODE-1's concise “2 sentences max + offer details” behavior.
        self.system_instruction = (
            """You are a concise robotic assistant. Answer in 1–2 sentences. If more explanation is needed, provide a 
            summary and ask if the user wants details. Strictly avoid using Markdown formatting like asterisks for bold 
            or italics. Write only in plain, spoken English. Use standard punctuation like periods and commas 
            for natural pauses."""
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
        with open("latest_response.txt", "w", encoding="utf-8") as file:
            file.write(text)
        return LlmResult(response_text=text)
