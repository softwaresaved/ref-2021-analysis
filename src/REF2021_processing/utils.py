""" Utilities for REF2021 processing. """
import os
import logging
import pandas as pd
import REF2021_processing.read_write as rw
import REF2021_processing.codebook as cb

COMPLETED_ICON = "\033[32m\u2713\033[0m"
FAILED_ICON = "\033[31m\u2717\033[0m"
LOGGING_FORMAT = "%(asctime)s [%(levelname)s] %(message)s"


def add_verbose_parser_argument(parser):
    """Add verbose parser argument.

    Args:
        parser (argparse.ArgumentParser): Parser.

    Returns:
        argparse.ArgumentParser: Parser with added verbose argument.
    """

    parser.add_argument(
        "-v",
        "--verbose",
        required=False,
        default=False,
        choices=[True, False],
        help="write logging to console, default false",
    )

    return parser


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
    except OSError as e:
        print(f"{FAILED_ICON} failed: setup logger {e}")
        return False

    handlers = [logging.FileHandler(fpath)]

    if verbose:
        handlers.append(logging.StreamHandler())

    logging.basicConfig(format=LOGGING_FORMAT, level=logging.INFO, handlers=handlers)
    return True


def complete_logger(source, verbose=True):
    """Complete logger.

    Args:
        source (str): Data source for the logged processing.
        verbose (bool): Print log messages to console.
    """

    try:
        fname = f"{source}{rw.LOGS['extension']}"
        fpath_interim = os.path.join(
            rw.PROJECT_PATH, f"{rw.LOGS['interim_path']}{fname}"
        )
        fpath = os.path.join(rw.PROJECT_PATH, f"{rw.LOGS['path']}{fname}")

        # move log file to the logs folder
        os.rename(fpath_interim, fpath)
        if verbose:
            print(f"{COMPLETED_ICON} moved log file to {fpath}")

        return True
    except OSError as e:
        print(f"{FAILED_ICON} failed: complete logger {e}")
        return False


def drop_specified_columns(dset, columns_to_drop, sname):
    """Drop specified columns from the dataset.

    Args:
        dset (pandas.DataFrame): Dataset.
        columns_to_drop (list): Columns to drop.
        sname (str): Source name.

    Returns:
        pandas.DataFrame: Dataset with specified columns dropped.
    """

    columns_to_drop = list(set(columns_to_drop).intersection(dset.columns))
    if len(columns_to_drop) > 0:
        dset = dset.drop(columns_to_drop, axis=1)
        logging.info("%s - drop columns '%s'", sname, columns_to_drop)

    return dset


def make_columns_categorical(dset, columns, sname):
    """Make specified columns categorical.

    Args:
        dset (pandas.DataFrame): Dataset.
        columns (list): Columns to make categorical.
        sname (str): Source name.

    Returns:
        pandas.DataFrame: Dataset with specified columns made categorical.
    """

    columns_to_category = list(set(columns).intersection(dset.columns))
    if len(columns_to_category) > 0:
        logging.info("%s - make categorical %s", sname, columns_to_category)
        for column in columns_to_category:
            dset[column] = pd.Categorical(dset[column])

    return dset


def fix_mult_sub_letter(dset, sname):
    """Fix mult sub letter column.

    Args:
        dset (pandas.DataFrame): Dataset.
        sname (str): Source name.

    Returns:
        pandas.DataFrame: Dataset with fixed mult sub letter column.
    """

    if cb.COL_MULT_SUB_LETTER in dset.columns:
        dset[cb.COL_MULT_SUB_LETTER] = dset[cb.COL_MULT_SUB_LETTER].fillna("")
        logging.info("%s - replace na with '' in %s", sname, cb.COL_MULT_SUB_LETTER)

    return dset


def get_info_from_filename(fname):
    """Get information from the filename.

    Args:
        fname (str): filename

    Returns:
        tuple: institution name, unit code, multiple submission letter
    """

    institution_name, unit_code_original = fname.split(" - ")

    # process tbe unit code and the multiple submission letter
    unit_code = "".join([i for i in unit_code_original if not i.isalpha()])
    multiple_submission_letter = ""
    if len(unit_code) != len(unit_code_original):
        multiple_submission_letter = unit_code_original[-1]

    return institution_name, unit_code, multiple_submission_letter
