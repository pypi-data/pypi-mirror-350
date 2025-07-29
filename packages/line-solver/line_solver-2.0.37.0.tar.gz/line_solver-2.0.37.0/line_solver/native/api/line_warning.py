import time
from line_solver import *

def line_printf(msg):
    print(msg)

def line_warning(caller, MSG, *args):
    # Persistent-like function attributes
    if not hasattr(line_warning, "lastWarning"):
        line_warning.lastWarning = ""
    if not hasattr(line_warning, "suppressedWarnings"):
        line_warning.suppressedWarnings = False
    if not hasattr(line_warning, "suppressedWarningsTic"):
        line_warning.suppressedWarningsTic = time.time()
    if not hasattr(line_warning, "lastWarningTime"):
        line_warning.lastWarningTime = time.time()
    if not hasattr(line_warning, "suppressedAnnouncement"):
        line_warning.suppressedAnnouncement = False

    if GlobalConstants.Verbose == VerboseLevel.SILENT:
        return

    errmsg = MSG % args
    finalmsg = f"Warning [{caller}.py]: {errmsg}"
    current_time = time.time()

    if (finalmsg != line_warning.lastWarning or
            (current_time - line_warning.lastWarningTime) > 60):
        line_printf(finalmsg)
        line_warning.lastWarning = finalmsg
        line_warning.suppressedWarnings = False
        line_warning.suppressedWarningsTic = current_time
        line_warning.suppressedAnnouncement = False
    else:
        if not line_warning.suppressedWarnings and not line_warning.suppressedAnnouncement:
            suppress_msg = (
                f"\nWarning [{caller}.py]: Warning message casted more than once, "
                "repetitions will not be printed on screen for 60 seconds.\n"
            )
            line_printf(suppress_msg)
            line_warning.suppressedAnnouncement = True
            line_warning.suppressedWarnings = True
            line_warning.suppressedWarningsTic = current_time

    line_warning.lastWarningTime = current_time
