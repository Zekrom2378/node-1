import time
from .events import Event, EventType, State
from .fsm import StateMachine
from .planner import GesturePlanner
from .mcu import MCUInterface
from .cloud import CloudClient
from .log import setup_logger

logger = setup_logger()

def run_main() -> None:
    fsm = StateMachine()
    planner = GesturePlanner()
    mcu = MCUInterface()
    cloud = CloudClient()

    # Enter initial state
    mcu.set_state(fsm.state.name)
    mcu.play_gesture(planner.on_enter_state(fsm.state))

    logger.info("Console controls: [s]=heard speech, [w]=wake word, [p]=prompt, [r]=reset, [q]=quit")

    while True:
        # Network Timeout Handling
        if fsm.timed_out():
            fsm.handle(Event(EventType.TIMEOUT))
            mcu.set_state(fsm.state.name)
            mcu.play_gesture(planner.on_enter_state(fsm.state))

        cmd = input("> ").strip().lower()
        if cmd == 'q':
            break

        if cmd == 's':
            fsm.handle(Event(EventType.HEARD_SPEECH))
        elif cmd == 'w':
            fsm.handle(Event(EventType.WAKE_WORD))
        elif cmd == 'p':
            text = input("prompt text: ").strip()
            fsm.handle(Event(EventType.PROMPT_TEXT, {"text": text}))
            # If a prompt is sent to the LLM, it will enter THINKING; call cloud stub and return the response
            if fsm.state == State.THINKING:
                result = cloud.run(fsm.ctx.prompt_text)
                fsm.handle(Event(EventType.LLM_RESULT, {"text": result.response_text}))
                plan = planner.plan_response(result.response_text)
                fsm.enter(plan.state_after)
                mcu.play_gesture(plan.gesture_id)
                logger.info(f"RESPONSE: {result.response_text}")
                # auto reset to idle after response for now
                fsm.handle(Event(EventType.RESET))
            elif cmd == "r":
                fsm.handle(Event(EventType.RESET))
            else:
                logger.info("Unknown command")

                # send state/gesture on any transition
            mcu.set_state(fsm.state.name)
            mcu.play_gesture(planner.on_enter_state(fsm.state))

            time.sleep(0.01)

        if __name__ == "__main__":
            run_main()
