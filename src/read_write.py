import os
import shutil
import pandas as pd
import codebook as cb
import preprocess as pp
import logs as lg

# logs
LOG_PATH = "logs/"
LOG_EXT = ".log"
LOG_SETUP = os.path.join(LOG_PATH, f"setup{LOG_EXT}")
LOG_UNZIP = os.path.join(LOG_PATH, f"unzip_environment_statements{LOG_EXT}")
LOG_EXTRACT = os.path.join(LOG_PATH, "extract_")
LOG_PPREPROCESS = os.path.join(LOG_PATH, "preprocess_")
LOG_PREPARE = os.path.join(LOG_PATH, "prepare_")

# data paths
PROJECT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
DATA_PATH = "data/"
RAW_PATH = os.path.join(DATA_PATH, "raw/")
RAW_ENV_PATH = os.path.join(RAW_PATH, "environment_statements/")
RAW_ENV_INST_PATH = os.path.join(RAW_ENV_PATH, "institution/")
RAW_ENV_UNIT_PATH = os.path.join(RAW_ENV_PATH, "unit/")
PROCESSED_SHEETS_PATH = os.path.join(DATA_PATH, "processed/sheets/")
PROCESSED_ENV_EXTRACTED_PATH = os.path.join(DATA_PATH, "processed/environment_statements/extracted/")
PROCESSED_ENV_PREPARED_PATH = os.path.join(DATA_PATH, "processed/environment_statements/prepared/")

REQUIRED_FOLDERS = [LOG_PATH,
                    PROCESSED_SHEETS_PATH,
                    PROCESSED_ENV_PREPARED_PATH
                    ]

# data files
RAW_SUBMISSIONS_FNAME = f"{RAW_PATH}REF-2021-Submissions-All-2022-07-27.xlsx"
RAW_SUBMISSIONS_HEADER_INDEX = 4
RAW_RESULTS_FNAME = f"{RAW_PATH}REF-2021-Results-All-2022-05-06.xlsx"
RAW_RESULTS_HEADER_INDEX = 6
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
DATA_EXTRACT_OUTPUTS = f"{PROCESSED_SHEETS_PATH}{sheet}{DATA_EXT}"
DATA_PPROC_OUTPUTS = f"{PROCESSED_SHEETS_PATH}{sheet}{DATA_PPROCESS}{DATA_EXT}"
# ImpactCaseStudies
sheet = SHEETS[1]
SHEET_IMPACTS = sheet
LOG_EXTRACT_IMPACTS = f"{LOG_EXTRACT}{sheet}{LOG_EXT}"
LOG_PPROC_IMPACTS = f"{LOG_PPREPROCESS}{sheet}{LOG_EXT}"
DATA_EXTRACT_IMPACTS = f"{PROCESSED_SHEETS_PATH}{sheet}{DATA_EXT}"
DATA_PPROC_IMPACTS = f"{PROCESSED_SHEETS_PATH}{sheet}{DATA_PPROCESS}{DATA_EXT}"
# ResearchDoctoralDegreesAwarded
sheet = SHEETS[2]
SHEET_DEGREES = sheet
LOG_EXTRACT_DEGREES = f"{LOG_EXTRACT}{sheet}{LOG_EXT}"
LOG_PPROC_DEGREES = f"{LOG_PPREPROCESS}{sheet}{LOG_EXT}"
DATA_EXTRACT_DEGREES = f"{PROCESSED_SHEETS_PATH}{sheet}{DATA_EXT}"
# ResearchIncome
sheet = SHEETS[3]
SHEET_INCOME = sheet
LOG_EXTRACT_INCOME = f"{LOG_EXTRACT}{sheet}{LOG_EXT}"
LOG_PPROC_INCOME = f"{LOG_PPREPROCESS}{sheet}{LOG_EXT}"
DATA_EXTRACT_INCOME = f"{PROCESSED_SHEETS_PATH}{sheet}{DATA_EXT}"
# ResearchIncomeInKind
sheet = SHEETS[4]
SHEET_INCOMEINKIND = sheet
LOG_EXTRACT_INCOMEINKIND = f"{LOG_EXTRACT}{sheet}{LOG_EXT}"
LOG_PPROC_INCOMEINKIND = f"{LOG_PPREPROCESS}{sheet}{LOG_EXT}"
DATA_EXTRACT_INCOMEINKIND = f"{PROCESSED_SHEETS_PATH}{sheet}{DATA_EXT}"
# ResearchGroups
sheet = SHEETS[5]
SHEET_RGROUPS = sheet
LOG_EXTRACT_RGROUPS = f"{LOG_EXTRACT}{sheet}{LOG_EXT}"
LOG_PPROC_RGROUPS = f"{LOG_PPREPROCESS}{sheet}{LOG_EXT}"
DATA_EXTRACT_RGROUPS = f"{PROCESSED_SHEETS_PATH}{sheet}{DATA_EXT}"
DATA_PPROC_RGROUPS = f"{PROCESSED_SHEETS_PATH}{sheet}{DATA_PPROCESS}{DATA_EXT}"
# Results
sheet = "Results"
SHEET_RESULTS = sheet
LOG_EXTRACT_RESULTS = f"{LOG_EXTRACT}{sheet}{LOG_EXT}"
LOG_PPROC_RESULTS = f"{LOG_PPREPROCESS}{sheet}{LOG_EXT}"
DATA_EXTRACT_RESULTS = f"{PROCESSED_SHEETS_PATH}{sheet}{DATA_EXT}"
DATA_PPROC_RESULTS = f"{PROCESSED_SHEETS_PATH}{sheet}{DATA_PPROCESS}{DATA_EXT}"

# environment statements
# ----------------------
ENV_INSTITUTION = "institution"
ENV_UNIT = "unit"
LOG_PREPARE_ENV_INSTITUTION = f"{LOG_PREPARE}environment_institution{LOG_EXT}"
LOG_PREPARE_ENV_UNIT = f"{LOG_PREPARE}environment_unit{LOG_EXT}"


def clean_folders():
    """ Clean the data folders if they exist.
    """
    cleaned_folder = False
    for path in REQUIRED_FOLDERS:
        if os.path.exists(path):
            shutil.rmtree(os.path.join(PROJECT_PATH, path))
            cleaned_folder = True
            lg.print_tstamp(f"DELETED '{path}'")

    if not cleaned_folder:
        lg.print_tstamp("None of the required folders need cleaning")


def create_folders():
    """ Create the data folders if they do not exist.
    """
    created_folder = False
    for path in REQUIRED_FOLDERS:
        if not os.path.exists(path):
            os.makedirs(os.path.join(PROJECT_PATH, path))
            created_folder = True
            lg.print_tstamp(f"CREATED '{path}'")

    if not created_folder:
        lg.print_tstamp("All required folders already exist")


def get_data(fname, do_sort=True):
    """ Read a csv file and return a dataset and a list of institution names.

    Args:
        fname (str): Filename of the csv file to read.
        do_sort (bool): If True, sort the institution names.

    Returns:
        tuple: A tuple containing:
            - pd.DataFrame: Dataset read from the csv file.
            - list: List of institution names
    """

    # defines types to read
    dtype = {cb.COL_INST_CODE: 'category',
             cb.COL_PANEL_NAME: 'category',
             cb.COL_UOA_NAME: 'category'
             }
    # binned percentages and various categories, depending on file
    binned_perc_columns = []
    categories_columns = []
    if "Results_" in fname:
        binned_perc_columns = [cb.COL_RESULTS_1star_BINNED,
                               cb.COL_RESULTS_2star_BINNED,
                               cb.COL_RESULTS_3star_BINNED,
                               cb.COL_RESULTS_4star_BINNED,
                               cb.COL_RESULTS_UNCLASSIFIED_BINNED,
                               cb.COL_RESULTS_PERC_STAFF_SUBMITTED_BINNED
                               ]
    elif "Outputs_" in fname:
        categories_columns = [cb.COL_OUTPUT_TYPE_NAME,
                              cb.COL_OPEN_ACCESS
                              ]

    for column in binned_perc_columns:
        dtype[column] = 'category'

    for column in categories_columns:
        dtype[column] = 'category'

    dset = pd.read_csv(os.path.join(PROJECT_PATH, fname),
                       index_col=None,
                       dtype=dtype)
    print(f"Read {fname}: {dset.shape[0]} records")

    # set the category order for the binned percentages
    for column in binned_perc_columns:
        dset[column] = pd.Categorical(dset[column],
                                      categories=pp.bin_percentages_labels(),
                                      ordered=True)

    # get institution names as list
    inst_names = dset[cb.COL_INST_NAME].unique()

    if do_sort:
        inst_names.sort()

    return (dset, inst_names)
