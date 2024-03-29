import logging
import platform
from threading import Thread
from time import sleep
from random import random
import keyboard
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    tk = None
    ttk = None
from keymaer.engine.delay import Delay


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
        self.press_delay = None
        if not press_delay:
            self._default_press_delay = Delay(0.02, 0.03)
        else:
            self.press_delay = Delay.from_dict(press_delay)
        self.remove = remove
        self._logger = logging.getLogger("KeyMap")
        if not tk or not ttk:
            self._logger.warning(
                "Tkinter is not installed. Input box will not work."
            )
        self._thread = None
        self._pressing = False
        self._input_box_open = False
        # Currently pressed keys
        self._timer_threads: dict[str:dict] = {}
        self._pressed_keys = []

    def press_key(self, target_key: str):
        self._pressing = True
        rnd_len = (self.press_delay or self._default_press_delay).random()
        self._logger.debug(f"Pressing {target_key} for {rnd_len} seconds")
        try:
            keyboard.press(target_key)
            sleep(rnd_len)
            keyboard.release(target_key)
        except ValueError:
            # Support typing unicode keys.
            keyboard.write(target_key)
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
        if not tk or not ttk:
            return
        if self._input_box_open:
            return
        self._logger.debug("Inititalizing input box...")
        self._input_box_open = True
        try:
            root = tk.Tk(className="keymaer")
        except tk.TclError as e:
            self._logger.warning(f"Could not create Tk window: {e}")
            return
        if platform.system() != "Linux":
            root.overrideredirect(1)
        root.geometry("96x20+0+0")
        root.attributes("-topmost", True)
        entry = ttk.Entry(root)
        entry.pack()

        # Callbacks
        def input_event(inp_str: str = None):
            if not isinstance(inp_str, str):
                inp_str = entry.get()
            self._logger.debug(f"String in box: {inp_str}")
            self._logger.debug("Destroying window...")
            root.destroy()
            if not inp_str:
                return
            if platform.system() == "Linux":
                # Wait for the window to close (because of window decorations)
                sleep(0.05)
            self._logger.debug("Pressing keys...")
            if self.press_delay:
                for key in inp_str:
                    keyboard.write(key)
                    sleep(self.press_delay.random())
                return
            keyboard.write(inp_str, delay=0.005)

        # Fixups
        def focus_input_box():
            self._logger.debug("Focusing input box...")
            root.focus_set()
            entry.focus_force()

        # Bind events
        root.bind("<FocusOut>", lambda _: root.destroy())
        root.bind("<Escape>", lambda _: root.destroy())
        root.bind("<Return>", input_event)
        # Focus
        sleep(0.05)
        self._logger.debug("Showing input box...")
        root.after(1, focus_input_box)
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
            f"Pressed: {self._pressed_keys} | Trigger: {self.trigger_keys} | Target: {self.target_key}"  # noqa: E501
        )
        timer_address = str(random())
        self._timer_threads[timer_address] = 0
        Thread(
            target=self._time_counter,
            args=[key_name, timer_address],
            daemon=True,
        ).start()
        if self._pressed_keys == self.trigger_keys:
            if self._input_box_open:
                return
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
