# killswitch.py - Handle graceful stop signal

import os

def is_killswitch_active() -> bool:
    """Return True if killswitch file exists."""
    return os.path.exists(os.path.expanduser("~/.stop_dikagpt"))

def create_killswitch():
    """Create killswitch file to stop running instance."""
    with open(os.path.expanduser("~/.stop_dikagpt"), "w") as f:
        f.write("stop")

def remove_killswitch():
    """Remove killswitch file (allow future runs)."""
    try:
        os.remove(os.path.expanduser("~/.stop_dikagpt"))
    except FileNotFoundError:
        pass
