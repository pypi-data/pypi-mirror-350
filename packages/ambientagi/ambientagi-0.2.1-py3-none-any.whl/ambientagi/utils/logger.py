# ambientagi/log_utils.py
import logging


def suppress_browser_use_logs(level=logging.WARNING):
    logging.getLogger("browser_use").setLevel(level)
