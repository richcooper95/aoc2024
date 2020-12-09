from . import run
import sys
import traceback

try:
  run()
except Exception as exc:
  traceback.print_exception(*sys.exc_info())
  sys.exit(exc)