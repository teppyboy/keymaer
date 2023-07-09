import logging
from threading import Thread
from time import sleep
from random import uniform, random
import keyboard
import tkinter as tk
from tkinter import ttk


class Delay:
    def __init__(self, min: float, max: float) -> None:
        self.min = min
        self.max = max

    def random(self) -> float:
        return uniform(self.min, self.max)

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
        self._thread = None
        self._pressing = False
        self._input_box_open = False
        # Currently pressed keys
        self._timer_threads: dict[str:dict] = {}
        self._pressed_keys = []

    def press_key(self, target_key: str):
        self._pressing = True
        rnd_len = uniform(self.press_delay.min, self.press_delay.max)
        self._logger.debug(f"Pressing {target_key} for {rnd_len} seconds")
        keyboard.press(target_key)
        sleep(rnd_len)
        keyboard.release(target_key)
        self._pressing = False

    def _time_counter(self, key_name: str, address: str):
        sleep(self.delay.max)
        ref = self._timer_threads[address]
        if ref == 0:
            try:
                self._logger.debug(f"Removing key {key_name} from pressed keys...")
                self._logger.debug(f"Pressed keys: {self._pressed_keys}")
                self._pressed_keys.remove(key_name)
            except ValueError:
                pass
        del ref
        return

    def _clear_timer_threads(self):
        for k in self._timer_threads.keys():
            self._timer_threads[k] = 1

    def _show_input_box(self):
        if self._input_box_open:
            return
        self._logger.debug("Inititalizing input box...")
        self._input_box_open = True
        root = tk.Tk(className="keymaer")
        root.geometry("96x20+0+0")
        root.overrideredirect(1)
        root.attributes("-topmost", True)
        entry = ttk.Entry(root)
        entry.pack()
        # Callbacks
        def input_event(_):
            inp_str = entry.get()
            self._logger.debug(f"String in box: {inp_str}")
            self._logger.debug("Destroying window...")
            root.destroy()
            if not inp_str:
                return
            self._logger.debug("Pressing keys...")
            keyboard.write(inp_str, delay=0.005)

        # Focus
        root.focus_set()
        entry.focus_force()
        # root.after_idle(focus_input_box)
        # Bind events
        # root.bind("<FocusOut>", lambda _: root.destroy())
        root.bind("<Return>", input_event)
        sleep(0.05)
        self._logger.debug("Showing input box...")
        root.mainloop()
        self._input_box_open = False

    # This is where actual magic happens
    def _callback(self, pressed_key: keyboard.KeyboardEvent):
        if pressed_key.event_type != "down":
            return
        key_name = pressed_key.name or pressed_key.scan_code
        if key_name not in self.trigger_keys:
            return
        if self._pressing:
            return
        self._pressed_keys.append(key_name)
        self._logger.debug(
            f"Pressed keys: {self._pressed_keys} | Trigger keys: {self.trigger_keys}"
        )  # noqa: E501
        timer_address = str(random())
        self._timer_threads[timer_address] = 0
        Thread(
            target=self._time_counter,
            args=[key_name, timer_address],
            daemon=True,
        ).start()
        if self._pressed_keys == self.trigger_keys:
            self._logger.debug("Clearing keys...")
            self._clear_timer_threads()
            self._pressed_keys.clear()
            keyboard.release(key_name)
            if self.remove:
                for _ in self.trigger_keys:
                    keyboard.press("backspace")
                    keyboard.release("backspace")
            if self.target_key == "input_box":
                Thread(target=self._show_input_box(), daemon=True).start()
                return
            Thread(target=self.press_key, args=[self.target_key], daemon=True).start()
            self._logger.debug(f"Pressed keys: {self._pressed_keys}")
            return
        if len(self._pressed_keys) >= len(self.trigger_keys):
            self._logger.debug("Triggered delete")
            for _ in range(len(self._pressed_keys) - len(self.trigger_keys) + 1):
                self._pressed_keys.pop(0)
            return

    def start_map(self):
        if self.delay.min > 0:

            def check():
                self._logger.debug(
                    f"Map started with delay min for key {self.target_key}"
                )
                while True:
                    key = keyboard.read_event()
                    Thread(target=self._callback, args=[key], daemon=True).start()
                    sleep(self.delay.min)

        else:

            def check():
                self._logger.debug(f"Map started for key {self.target_key}")
                while True:
                    key = keyboard.read_event()
                    Thread(target=self._callback, args=[key], daemon=True).start()

        self._thread = Thread(target=check, daemon=True).start()
        self._logger.debug("Check thread started.")

    def stop_map(self):
        if self._thread:
            self._thread.stop()
        self._logger.debug("Check thread stopped.")
