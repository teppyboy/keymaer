import pyjion

from .app import main  # noqa: E402


print(vars(pyjion.info(main)))
main()
