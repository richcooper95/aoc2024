from . import run
import sys

try:
  run()
except Exception as exc:
  sys.exit(exc)