import time
import threading
from events import Event, EventType, State
from fsm import StateMachine
from planner import GesturePlanner
from mcu import MCUInterface
from cloud import CloudClient, ListModels
from log import setup_logger
from listener import Listener
from voice import VoiceEngine as voice_engine

logger = setup_logger()


def voice_input_thread(fsm_ref):
    listener = Listener()
    while True:
        # This will block, but only in this sub-thread
        event = listener.listen(fsm_ref.state)
        if event:
            fsm_ref.handle(event)


def run_main() -> None:
    fsm = StateMachine()
    planner = GesturePlanner()
    mcu = MCUInterface()
    cloud = CloudClient()
    voice = voice_engine(gender='m')
    # listener = Listener()

    # Enter initial state
    mcu.set_state(fsm.state.name)
    mcu.play_gesture(planner.on_enter_state(fsm.state))
    threading.Thread(target=voice_input_thread, args=(fsm,), daemon=True).start()

    logger.info("Console controls: [s]=heard speech, [w]=wake word, [p]=prompt, [r]=reset, [q]=quit")

    while True:
        # 1. Check for Timeouts
        if fsm.timed_out():
            fsm.handle(Event(EventType.TIMEOUT))

        # 3. Logic for THINKING
        if fsm.state == State.THINKING:
            # Senior EE Tip: Use this delay to trigger the 'thinking' servos/LEDs
            mcu.play_gesture("thinking_sway")

            result = cloud.run(fsm.ctx.prompt_text)

            # Artificial delay for 'liveliness' as requested
            time.sleep(1.5)

            fsm.handle(Event(EventType.LLM_RESULT, {"text": result.response_text}))

            # 4. Logic for RESPONDING
            plan = planner.plan_response(result.response_text)
            fsm.enter(plan.state_after)
            mcu.play_gesture(plan.gesture_id)

            # Speak the result
            voice.speak(result.response_text)

            # Reset back to IDLE
            fsm.handle(Event(EventType.RESET))
        mcu.set_state(fsm.state.name)

        time.sleep(0.02)


if __name__ == '__main__':
    print("NODE-1 Main Starting")
    # ListModels()
    run_main()
