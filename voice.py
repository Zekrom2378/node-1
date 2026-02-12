import subprocess
from log import setup_logger

logger = setup_logger()


class VoiceEngine:
    def __init__(self, gender: str = "m"):
        # Windows usually needs the full path or just "espeak-ng" if in PATH
        self.executable = "espeak-ng"
        self.voice = "en-us+m3" if gender == "m" else "en-us+f3"

    def speak(self, text: str):
        try:
            # -v: voice, -s: speed (150 is steady), -p: pitch (50 is monotone)
            subprocess.run([self.executable, f"-v{self.voice}", "-s150", "-p50", text], check=True)
        except FileNotFoundError:
            logger.error("espeak-ng not found. Install it and add to PATH.")

# To use this, you'll need to install: sudo apt-get install espeak-ng