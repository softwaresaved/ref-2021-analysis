import os
import shutil
import datetime

# logs
LOG_PATH = "logs/"
LOG_EXT = ".log"
LOG_SETUP = os.path.join(LOG_PATH, f"setup{LOG_EXT}")
LOG_UNZIP = os.path.join(LOG_PATH, f"unzip_environment_statements{LOG_EXT}")
LOG_EXTRACT = os.path.join(LOG_PATH, "extract_")
LOG_PPREPROCESS = os.path.join(LOG_PATH, "preprocess_")

# data paths
PROJECT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
DATA_PATH = "data/"
RAW_PATH = os.path.join(DATA_PATH, "raw/")
ENV_PATH = os.path.join(RAW_PATH, "environment_statements/")
ENV_INST_PATH = os.path.join(ENV_PATH, "institution/")
ENV_UNIT_PATH = os.path.join(ENV_PATH, "unit/")
PROCESSED_PATH = os.path.join(DATA_PATH, "processed/")
SUBSETS_PATH = os.path.join(PROCESSED_PATH, "subsets/")

REQUIRED_FOLDERS = [LOG_PATH,
                    PROCESSED_PATH,
                    SUBSETS_PATH
                    ]

# data files
RAW_FNAME = f"{RAW_PATH}REF-2021-Submissions-All-2022-07-27.xlsx"
ENV_FNAME = f"{RAW_PATH}REF-2021-EnvironmentStatements-Extract-2023-08-22.zip"
SHEETS = ["Outputs",
          "ImpactCaseStudies",
          "ResearchDoctoralDegreesAwarded",
          "ResearchIncome",
          "ResearchIncomeInKind",
          "ResearchGroups"]
DATA_EXT = ".csv.gz"
DATA_PPROCESS = "_ppreprocessed"

# logs and output files
# ---------------------
# Outputs
sheet = SHEETS[0]
SHEET_OUTPUTS = sheet
LOG_EXTRACT_OUTPUTS = f"{LOG_EXTRACT}{sheet}{LOG_EXT}"
LOG_PPROC_OUTPUTS = f"{LOG_PPREPROCESS}{sheet}{LOG_EXT}"
DATA_EXTRACT_OUTPUTS = f"{PROCESSED_PATH}{sheet}{DATA_EXT}"
DATA_PPROC_OUTPUTS = f"{PROCESSED_PATH}{sheet}{DATA_PPROCESS}{DATA_EXT}"
DATA_PPROC_OUTPUTS_SOFTWARE_TYPES = f"{SUBSETS_PATH}{sheet}{DATA_PPROCESS}"\
                                    f"_type_software{DATA_EXT}"
DATA_PPROC_OUTPUTS_SOFTWARE_TERMS = f"{SUBSETS_PATH}{sheet}{DATA_PPROCESS}"\
                                    f"_title_software_terms{DATA_EXT}"
# ImpactCaseStudies
sheet = SHEETS[1]
SHEET_IMPACTS = sheet
LOG_EXTRACT_IMPACTS = f"{LOG_EXTRACT}{sheet}{LOG_EXT}"
LOG_PPROC_IMPACTS = f"{LOG_PPREPROCESS}{sheet}{LOG_EXT}"
DATA_EXTRACT_IMPACTS = f"{PROCESSED_PATH}{sheet}{DATA_EXT}"
DATA_PPROC_IMPACTS = f"{PROCESSED_PATH}{sheet}{DATA_PPROCESS}{DATA_EXT}"
DATA_PPROC_IMPACTS_SOFTWARE_TERMS = f"{SUBSETS_PATH}{sheet}{DATA_PPROCESS}"\
                                     f"_title_summary_software_terms{DATA_EXT}"
# ResearchDoctoralDegreesAwarded
sheet = SHEETS[2]
SHEET_DEGREES = sheet
LOG_EXTRACT_DEGREES = f"{LOG_EXTRACT}{sheet}{LOG_EXT}"
LOG_PPROC_DEGREES = f"{LOG_PPREPROCESS}{sheet}{LOG_EXT}"
DATA_EXTRACT_DEGREES = f"{PROCESSED_PATH}{sheet}{DATA_EXT}"
# ResearchIncome
sheet = SHEETS[3]
SHEET_INCOME = sheet
LOG_EXTRACT_INCOME = f"{LOG_EXTRACT}{sheet}{LOG_EXT}"
LOG_PPROC_INCOME = f"{LOG_PPREPROCESS}{sheet}{LOG_EXT}"
DATA_EXTRACT_INCOME = f"{PROCESSED_PATH}{sheet}{DATA_EXT}"
# ResearchIncomeInKind
sheet = SHEETS[4]
SHEET_INCOMEINKIND = sheet
LOG_EXTRACT_INCOMEINKIND = f"{LOG_EXTRACT}{sheet}{LOG_EXT}"
LOG_PPROC_INCOMEINKIND = f"{LOG_PPREPROCESS}{sheet}{LOG_EXT}"
DATA_EXTRACT_INCOMEINKIND = f"{PROCESSED_PATH}{sheet}{DATA_EXT}"
# ResearchGroups
sheet = SHEETS[5]
SHEET_RGROUPS = sheet
LOG_EXTRACT_RGROUPS = f"{LOG_EXTRACT}{sheet}{LOG_EXT}"
LOG_PPROC_RGROUPS = f"{LOG_PPREPROCESS}{sheet}{LOG_EXT}"
DATA_EXTRACT_RGROUPS = f"{PROCESSED_PATH}{sheet}{DATA_EXT}"
DATA_PPROC_RGROUPS = f"{PROCESSED_PATH}{sheet}{DATA_PPROCESS}{DATA_EXT}"


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
