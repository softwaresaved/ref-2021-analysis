import os
import shutil
import datetime

# data paths
PROJECT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
LOGS_PATH = "logs/"
DATA_PATH = "data/"
RAW_PATH = os.path.join(DATA_PATH, "raw/")
PROCESSED_PATH = os.path.join(DATA_PATH, "processed/")
PROCESSED_EXTRACTED_PATH = os.path.join(PROCESSED_PATH, "extracted/")
PROCESSSED_SUBSETS_PATH = os.path.join(PROCESSED_PATH, "subsets/")

REQUIRED_FOLDERS = [LOGS_PATH,
                    PROCESSED_EXTRACTED_PATH,
                    PROCESSSED_SUBSETS_PATH
                    ]


def print_tstamp(text):
    """ Print a timestamped message.

    Args:
        text (str): The message to print.
    """

    now = datetime.datetime.now()
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {text}")


def clean_folders():
    """ Clean the data folders if they exist.
    """
    cleaned_folder = False
    for path in REQUIRED_FOLDERS:
        if os.path.exists(path):
            shutil.rmtree(os.path.join(PROJECT_PATH, path))
            cleaned_folder = True
            print_tstamp(f"DELETED '{path}'")

    if not cleaned_folder:
        print_tstamp("None of the required folders need cleaning")


def create_folders():
    """ Create the data folders if they do not exist.
    """
    created_folder = False
    for path in REQUIRED_FOLDERS:
        if not os.path.exists(path):
            os.makedirs(os.path.join(PROJECT_PATH, path))
            created_folder = True
            print_tstamp(f"CREATED '{path}'")

    if not created_folder:
        print_tstamp("All required folders already exist")
