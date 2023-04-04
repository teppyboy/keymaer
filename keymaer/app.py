import keyboard
import os
import getpass
from threading import Thread
from time import sleep
import platform
import json


CFG_DIRS = ["config.json"]
if platform.system() == "Linux":
    if os.getuid() != 0:
        # Not su
        CFG_DIRS.extend([f"/home/{getpass.getuser()}/.keymaer/config.json"])
    CFG_DIRS.extend(["/etc/keymaer/config.json"])


def read_cfg():
    cfg = None
    for file in CFG_DIRS:
        print("Reading config from", file)
        try:
            cfg = json.load(open(file=file))
            break
        except Exception:
            continue
    return cfg


def register_key(
    target_key: str, trigger: list[str], delay_min: float, delay_max: float, remove=True
):
    print(f"Registering {target_key} with trigger {trigger}...")
    print(f"Delay {delay_min} / {delay_max}, remove keypress {remove}")
    cur_keys = []

    def counter(key_name):
        sleep(delay_max)
        try:
            cur_keys.remove(key_name)
        except ValueError:
            return

    def press_key():
        keyboard.press(target_key)
        sleep(0.03)
        keyboard.release(target_key)

    def callback(cur_key):
        if cur_key.event_type != "down":
            return
        key_name = cur_key.name or cur_key.scan_code
        if key_name not in trigger:
            return
        cur_keys.append(key_name)
        print(cur_keys, trigger)
        if cur_keys == trigger:
            keyboard.release(key_name)
            if remove:
                for _ in trigger:
                    keyboard.press("backspace")
                    keyboard.release("backspace")
            Thread(target=press_key, daemon=True).start()
            cur_keys.clear()
            return
        if len(cur_keys) >= len(trigger):
            for i in range(len(cur_keys) - len(trigger)):
                cur_keys.pop(i)
            return
        Thread(target=counter, args=[key_name], daemon=True).start()

    if delay_min > 0:
        def check():
            print("Check started with delay min for key", target_key)
            while True:
                cur_key = keyboard.read_event()
                callback(cur_key)
                sleep(delay_min)
    else:
        def check():
            print("Check started for key", target_key)
            while True:
                cur_key = keyboard.read_event()
                callback(cur_key)

    Thread(target=check, daemon=True).start()


def main():
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
