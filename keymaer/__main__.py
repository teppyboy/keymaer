import pyjion
pyjion.config(level=2, pgc=False)
if pyjion.enable():
    print("EXPERIMENTAL: Pyjion optimization enabled")
    print("Pyjion may takes up to 30 seconds to properly optimize the code.")
    print("During JIT optimization, your system will be unresponsive.")
from .app import main  # noqa: E402
print(vars(pyjion.info(main)))
main()
