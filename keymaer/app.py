import keyboard
from threading import Thread
from time import sleep
import json


def read_cfg():
    try:
        return json.load(open("config.json"))
    except Exception:
        return None


def register_key(
    target_key: str, trigger: list[str], delay_min: float, delay_max: float, remove=True
):
    print(f"Registering {target_key} with trigger {trigger}...")
    print(f"Delay {delay_min} / {delay_max}, remove keypress {remove}")
    cur_keys = []

    def callback(cur_key):
        if cur_key.event_type != "down":
            return
        key_name = cur_key.name
        if key_name not in trigger:
            return
        cur_keys.append(key_name)
        print(cur_keys, trigger)
        if cur_keys == trigger:
            if remove:
                for _ in trigger:
                    keyboard.press("backspace")
                    keyboard.release("backspace")
            keyboard.press(target_key)
            sleep(0.03)
            keyboard.release(target_key)
            cur_keys.clear()
            return
        elif len(cur_keys) >= len(trigger):
            cur_keys.clear()
            return

        def counter():
            sleep(delay_max)
            try:
                cur_keys.remove(key_name)
            except ValueError:
                return

        Thread(target=counter, daemon=True).start()

    def check():
        print("Check started for key", target_key)
        while True:
            cur_key = keyboard.read_event()
            callback(cur_key)
            sleep(delay_min)

    Thread(target=check, daemon=True).start()


def main():
    print("Reading configuration...")
    cfg = read_cfg()
    delay = cfg["delay"]
    for key in cfg["keys"]:
        print(f"Registering key {key}...")
        if cfg.get("delay"):
            max_delay = cfg["delay"]["max"]
            min_delay = cfg["delay"]["min"]
        else:
            max_delay = delay["max"]
            min_delay = delay["min"]
        register_key(
            target_key=key["key"],
            trigger=key["trigger"],
            delay_min=min_delay,
            delay_max=max_delay,
        )
    print("Press Ctrl + C to exit program.")
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("Exiting...")
