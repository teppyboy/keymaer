import logging
from threading import Thread
from time import sleep
from random import uniform
import keyboard


class Delay:
    def __init__(self, min: float, max: float) -> None:
        self.min = min
        self.max = max

    @staticmethod
    def from_dict(delay_dict: dict) -> "Delay":
        return Delay(delay_dict["min"], delay_dict["max"])


class KeyMap:
    def __init__(
        self,
        target_key: str,
        trigger_keys: list[str],
        delay: Delay,
        press_delay: Delay = None,
        remove: bool = True,
    ) -> None:
        self.target_key = target_key
        self.trigger_keys = trigger_keys
        self.delay = delay
        if not press_delay:
            press_delay = Delay(0.02, 0.03)
        self.press_delay = press_delay
        self.remove = remove
        self._logger = logging.getLogger("KeyMap")
        # Currently pressed keys
        self._pressed_keys = []

    def press_key(self):
        keyboard.press(self.target_key)
        rnd_len = uniform(self.press_delay.min, self.press_delay.max)
        self._logger.debug(f"Pressing {self.target_key} for {rnd_len} seconds")
        sleep(rnd_len)
        keyboard.release(self.target_key)

    def _time_counter(self, key_name: str):
        sleep(self.delay.max)
        try:
            self._pressed_keys.remove(key_name)
        except ValueError:
            return

    # This is where actual magic happens
    def _callback(self, pressed_key: keyboard.KeyboardEvent):
        if pressed_key.event_type != "down":
            return
        key_name = pressed_key.name or pressed_key.scan_code
        if key_name not in self.trigger_keys:
            return
        self._pressed_keys.append(key_name)
        self._logger.debug(
            f"Pressed keys: {self._pressed_keys} | Trigger keys: {self.trigger_keys}"
        )  # noqa: E501
        if self._pressed_keys == self.trigger_keys:
            keyboard.release(key_name)
            if self.remove:
                for _ in self.trigger_keys:
                    keyboard.press("backspace")
                    keyboard.release("backspace")
            Thread(target=self.press_key, daemon=True).start()
            self._pressed_keys.clear()
            return
        if len(self._pressed_keys) >= len(self.trigger_keys):
            for i in range(len(self._pressed_keys) - len(self.trigger_keys)):
                self._pressed_keys.pop(i)
            return
        Thread(target=self._time_counter, args=[key_name], daemon=True).start()

    def start_map(self):
        if self.delay.min > 0:

            def check():
                self._logger.debug(
                    "Map started with delay min for key", self.target_key
                )
                while True:
                    key = keyboard.read_event()
                    self._callback(key)
                    sleep(self.delay.min)

        else:

            def check():
                self._logger.debug("Map started for key", self.target_key)
                while True:
                    key = keyboard.read_event()
                    self._callback(key)

        Thread(target=check, daemon=True).start()
        self._logger.debug("Check thread started.")
