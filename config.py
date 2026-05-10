# config.py - Central configuration

KILLSWITCH_PATH = "~/.stop_dikagpt"
DEFAULT_MESSAGE_TEMPLATE = "DIKAGPT-X @COUNT@ @TIMESTAMP@"
DEFAULT_RATE = 20          # messages per second (use with caution)
DEFAULT_COUNT = 60         # total messages
DEFAULT_DELAY_JITTER = 0.005  # small random jitter to avoid detection
