import speech_recognition as sr
from events import Event, EventType, State
from log import setup_logger
import fsm

logger = setup_logger()


class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    def listen(self, current_state: State) -> Event:
        with self.mic as source:
            logger.info(f"Listening (State: {current_state.name})...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.3)
            try:
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=5.0)
                text = self.recognizer.recognize_google(audio).lower()
                logger.info(f"Heard: {text}")

                # Logic to determine Event
                if current_state == State.IDLE:
                    if "node" in text:
                        return Event(EventType.WAKE_WORD, {"text": text})
                    return Event(EventType.HEARD_SPEECH, {"text": text})

                elif current_state == State.ATTENTIVE:
                    if "node" in text:
                        return Event(EventType.WAKE_WORD, {"text": text})

                elif current_state == State.LISTENING:
                    return Event(EventType.PROMPT_TEXT, {"text": text})

                return None
            except Exception:
                return None

    def process_audio(text: str, current_state: State):
        text = text.lower()

        if current_state == State.IDLE:
            # Any speech moves it to Attentive
            return Event(EventType.HEARD_SPEECH)

        elif current_state == State.ATTENTIVE:
            if "node" in text:  # Replace with your wake word
                return Event(EventType.WAKE_WORD)
            return None  # Stay in Attentive or wait for timeout

        elif current_state == State.LISTENING:
            # In this state, the speech IS the prompt
            return Event(EventType.PROMPT_TEXT, {"text": text})

        return None
