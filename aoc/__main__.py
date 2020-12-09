from . import run
import sys
import traceback

try:
  run()
except Exception as exc:
  traceback.print_exc(exc)
  sys.exit(exc)