import os
import logging
import REF2021_processing.read_write as rw

COMPLETED_ICON = "\033[32m\u2713\033[0m"
FAILED_ICON = "\033[31m\u2717\033[0m"
LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"


def setup_logger(prefix, verbose=True):
    """Setup logger.

    Args:
        prefix (str): Prefix for the log file name.
        verbose (bool): Print log messages to console.
    """

    try:
        fname = f"{prefix}.log"
        # make folders that do not exist and delete previous log files
        for fpath in [rw.LOG_PATH, rw.LOG_INTERIM_PATH]:
            if not os.path.exists(fpath):
                os.makedirs(fpath)
            if os.path.exists(f"{fpath}{fname}"):
                os.remove(f"{fpath}{fname}")

        handlers = [logging.FileHandler(f"{rw.LOG_INTERIM_PATH}{fname}")]

        if verbose:
            handlers.append(logging.StreamHandler())

        logging.basicConfig(format=LOGGING_FORMAT,
                            level=logging.INFO,
                            handlers=handlers)
        return True
    except Exception as e:
        print(f"{FAILED_ICON} failed: setup logger {e}")
        return False
