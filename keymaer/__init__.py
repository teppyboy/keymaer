import pyjion
pyjion.config(level=2, pgc=False)
if pyjion.enable():
    print("EXPERIMENTAL: Pyjion optimization enabled")
    print("Pyjion may takes up to 30 seconds to properly optimize the code.")
    print("During JIT optimization, your system will be unresponsive.")

from keymaer.engine import Delay, KeyMap  # noqa: E402


__all__ = ["Delay", "KeyMap"]
__version__ = "0.1.0"
