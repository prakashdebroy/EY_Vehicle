import time
import os

import eventlet
eventlet.monkey_patch()

from dotenv import load_dotenv
from sensors import SensorSource
from rules import evaluate
from state import StateMemory
from voice import speak
from llm_gemini import init_gemini, craft_line

from dashboard import app, socketio, set_shared_state

shared_state = {
    "sensors": None,
    "alerts": []
}

def sensor_loop(source):
    while True:
        sensors = source.read()
        alerts = evaluate(sensors)

        shared_state["sensors"] = sensors
        shared_state["alerts"] = alerts

        socketio.emit(
            "sensor_update",
            {
                "sensors": sensors,
                "alerts": [a.__dict__ for a in alerts]
            }
        )

        eventlet.sleep(1)


def voice_loop(memory, model):
    last_spoken = None

    while True:
        sensors = shared_state["sensors"]
        alerts = shared_state["alerts"]

        if not sensors:
            eventlet.sleep(2)
            continue

        speak_now = memory.should_speak(alerts)

        if speak_now:
            line = craft_line(model, sensors, alerts) if alerts else "All systems normal."
            print("SAY:", line)
            speak(line)

        eventlet.sleep(5)


def main():
    load_dotenv()

    source = SensorSource(mode="mock")
    model = init_gemini()
    memory = StateMemory()

    set_shared_state(shared_state)

    eventlet.spawn(sensor_loop, source)
    eventlet.spawn(voice_loop, memory, model)

    print("Dashboard running at http://localhost:5001")
    socketio.run(app, host="0.0.0.0", port=5001, debug=False)


if __name__ == "__main__":
    main()
