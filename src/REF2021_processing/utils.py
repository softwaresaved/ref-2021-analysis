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
        fname = f"{source}{rw.LOGS['extension']}"
        fpath = os.path.join(rw.PROJECT_PATH, f"{rw.LOGS['interim_path']}{fname}")

        # make folders that do not exist and delete previous log files
        for folder in [rw.LOGS["path"], rw.LOGS["interim_path"]]:
            if not os.path.exists(folder):
                os.makedirs(folder)
            if os.path.exists(f"{folder}{fname}"):
                os.remove(f"{folder}{fname}")

        handlers = [logging.FileHandler(fpath)]

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
        fname = f"{source}{rw.LOGS['extension']}"
        fpath_interim = os.path.join(rw.PROJECT_PATH, f"{rw.LOGS['interim_path']}{fname}")
        fpath = os.path.join(rw.PROJECT_PATH, f"{rw.LOGS['path']}{fname}")

        # move log file to the logs folder
        os.rename(fpath_interim, fpath)

        return True
    except Exception as e:
        print(f"{FAILED_ICON} failed: complete logger {e}")
        return False
