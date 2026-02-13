import subprocess
from log import setup_logger

logger = setup_logger()


class VoiceEngine:
    def __init__(self, gender: str = "m"):
        # Usually needs the full path or just "espeak-ng" if in PATH
        self.executable = "espeak-ng"
        self.voice = "en-us+m3" if gender == "m" else "en-us+f3"
        self.symbol_map = {
            "Ω": "ohms",
            "μ": "micro",
            "π": "pie",
            "ζ": "zay-ta",
            "∠": "at an angle of",
            "Δ": "delta",
            "∞": "infinity",
            "≈": "approximately",
            "×": "times",
            "°": "degrees"
        }

    def _clean_text(self, text: str) -> str:
        """Replaces engineering symbols with words for the TTS engine."""
        for symbol, word in self.symbol_map.items():
            text = text.replace(symbol, word)
        return text

    def speak(self, text: str):
        phonetic_text = self._clean_text(text)

        try:
            subprocess.run([
                self.executable,
                f"-v{self.voice}",
                "-s160",
                "-p60",
                phonetic_text
            ], check=True)
        except subprocess.CalledProcessError as e:
            logger.error(f"Voice output failed: {e}")
        except FileNotFoundError:
            logger.error("espeak-ng not found. Install it and add to PATH.")