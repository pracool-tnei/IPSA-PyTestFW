import builtins
import inspect
import os
from datetime import datetime

# Save original print
_original_print = builtins.print

from colorama import init, Fore, Style

init(autoreset=True)

DEBUG_MODE = True

# ANSI Colors
BLUE = "\033[94m"
RED = "\033[91m"
WHITE = "\033[97m"
RESET = "\033[0m"

def _log(level, color, *args, **kwargs):

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if DEBUG_MODE:
        frame = inspect.currentframe().f_back.f_back

        filename = os.path.basename(frame.f_code.co_filename)
        lineno = frame.f_lineno
        function = frame.f_code.co_name

        prefix = (
            f"[{timestamp}] "
            f"[{filename}:{lineno}] "
            f"[{function}] "
            f"[{level}]"
        )
    else:
        prefix = f"[{timestamp}] [{level}]"

    _original_print(
        color + prefix,
        *args,
        RESET,
        **kwargs
    )


def debug(*args, **kwargs):
    _log("D", WHITE, *args, **kwargs)


def info(*args, **kwargs):
    _log("I", BLUE, *args, **kwargs)


def error(*args, **kwargs):
    _log("E", RED, *args, **kwargs)

def setLoggerMode(mode):
    debug("Set Debug Mode : " + str(mode))
    global DEBUG_MODE
    DEBUG_MODE = mode