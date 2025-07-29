import inspect
import os


def mfilename():
    """
    Mimics MATLAB's mfilename by returning the name of the current script or function.
    """
    # Get the current call stack
    frame = inspect.currentframe()
    # Go back one level to the caller of mfilename
    caller_frame = frame.f_back
    # Get the filename from the caller's frame
    filename = caller_frame.f_globals.get('__file__', None)

    if filename:
        # Return the base name without extension
        return os.path.splitext(os.path.basename(filename))[0]
    else:
        # For interactive sessions (e.g., IPython), __file__ may not exist
        return "__main__"
