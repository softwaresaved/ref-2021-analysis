import os
import logging
import REF2021_processing.read_write as rw

COMPLETED_ICON = "\033[32m\u2713\033[0m"
FAILED_ICON = "\033[31m\u2717\033[0m"
LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"


def setup_logger(source, verbose=True):
    """Setup logger.

    Args:
        source (str): data source for the logged processing
        verbose (bool): Print log messages to console.
    """

    try:
        fname = f"{source}{rw.extensions['logs']}"
        # make folders that do not exist and delete previous log files
        for fpath in [rw.paths["logs"], rw.paths["logs_interim"]]:
            if not os.path.exists(fpath):
                os.makedirs(fpath)
            if os.path.exists(f"{fpath}{fname}"):
                os.remove(f"{fpath}{fname}")

        handlers = [logging.FileHandler(f"{rw.paths['logs_interim']}{fname}")]

        if verbose:
            handlers.append(logging.StreamHandler())

        logging.basicConfig(format=LOGGING_FORMAT,
                            level=logging.INFO,
                            handlers=handlers)
        return True
    except Exception as e:
        print(f"{FAILED_ICON} failed: setup logger {e}")
        return False


def complete_logger(source, verbose=True):
    """Complete logger.

    Args:
        source (str): Data source for the logged processing.
        verbose (bool): Print log messages to console.
    """

    try:
        fname = f"{source}{rw.extensions['logs']}"
        # move log file to the logs folder
        os.rename(f"{rw.paths['logs_interim']}{fname}",
                  f"{rw.paths['logs']}{fname}")

        return True
    except Exception as e:
        print(f"{FAILED_ICON} failed: complete logger {e}")
        return False
