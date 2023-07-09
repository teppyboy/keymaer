import keyboard
import logging
import platform
import json

from keymaer.engine import Delay, KeyMap
from keymaer.utils import setup_logging
from pathlib import Path
from sys import argv

CFG_DIRS = [
    "config.json",
    f"{Path.home()}/.keymaer/config.json",
    f"{Path.home()}/.keymaer.json",
    f"{Path.home()}/.config/keymaer.json",
]
match platform.system():
    case "Linux":
        CFG_DIRS.extend(["/etc/keymaer/config.json"])


def read_cfg():
    cfg = None
    for file in CFG_DIRS:
        print(f"Reading config from {file}")
        try:
            cfg = json.load(open(file=file))
            break
        except Exception:
            continue
    return cfg


def fix_key(key: str) -> str:
    if platform.system() == "Windows":
        if key == "−":
            return "-"
    return key


def fix_key_trigger(key_list: list[str]) -> list[str]:
    for i, key in enumerate(key_list):
        key_list[i] = fix_key(key)
    return key_list


def main():
    setup_logging()
    for i, arg in enumerate(argv):
        if arg == "--debug":
            logging.info("Setting debug logging...")
            logging.getLogger().setLevel(logging.DEBUG)
        if arg in ["-C", "--config"]:
            if len(argv) > i + 1:
                print(f"Adding {argv[i + 1]} to config search path...")
                CFG_DIRS.insert(0, argv[i + 1])
    logging.debug("Starting keymaer with DEBUG logging...")
    cfg = read_cfg()
    if not cfg:
        print("No config found, exiting...")
        return
    for key in cfg["keys"]:
        print(f"Registering key {key}...")
        if key.get("delay"):
            delay = Delay.from_dict(key["delay"])
        else:
            delay = Delay.from_dict(cfg["delay"])
        KeyMap(
            target_key=key["key"],
            trigger_keys=fix_key_trigger(key["trigger"]),
            delay=delay,
            remove=key.get("remove", True),
            press_delay=key.get("press_delay", None),
        ).start_map()
    print("Press Ctrl + C to exit program.")
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("Exiting...")
