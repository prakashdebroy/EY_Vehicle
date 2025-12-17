from typing import Any

class StateMemory:
    def __init__(self):
        self.last_signature = None

    def _signature(self, alerts):
        # compress to stable signature so we speak only when meaningfully changed
        return tuple(sorted((a.code, a.level) for a in alerts))

    def should_speak(self, alerts) -> bool:
        sig = self._signature(alerts)
        if sig != self.last_signature:
            self.last_signature = sig
            return True
        return False
