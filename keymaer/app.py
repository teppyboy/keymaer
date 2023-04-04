import keyboard
import logging
import os
import getpass
import platform
import json

from keymaer.classes import Delay, KeyMap
from keymaer.utils import setup_logging


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


def main():
    setup_logging()
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
            trigger_keys=key["trigger"],
            delay=delay,
            remove=key.get("remove", True),
        ).start_map()
    print("Press Ctrl + C to exit program.")
    try:
        keyboard.wait()
    except KeyboardInterrupt:
        print("Exiting...")
