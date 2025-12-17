# voice.py — CAR-SAFE VERSION

import pyttsx3
import threading
import queue
import time

_engine = None
_queue = queue.PriorityQueue()
_worker_started = False

# Priority: lower number = higher priority
CRITICAL = 0
NORMAL = 5

def _init_engine():
    global _engine
    if _engine is None:
        engine = pyttsx3.init("sapi5")
        engine.setProperty("rate", 165)   # car-friendly clarity
        engine.setProperty("volume", 1.0)

        # Optional: force male/female voice
        voices = engine.getProperty("voices")
        engine.setProperty("voice", voices[0].id)

        _engine = engine
    return _engine


def speak(text: str, priority=NORMAL):
    if not text or not text.strip():
        return

    _start_worker()
    _queue.put((priority, time.time(), text))


def interrupt_and_speak(text: str):
    _clear_queue()
    speak(text, priority=CRITICAL)


def _start_worker():
    global _worker_started
    if _worker_started:
        return

    _worker_started = True
    threading.Thread(target=_speech_worker, daemon=True).start()


def _speech_worker():
    engine = _init_engine()

    while True:
        priority, _, text = _queue.get()

        try:
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            print("TTS error:", e)

        _queue.task_done()


def _clear_queue():
    while not _queue.empty():
        try:
            _queue.get_nowait()
            _queue.task_done()
        except queue.Empty:
            break
