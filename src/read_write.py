import os
# import shutil
import pandas as pd
import logging

import codebook as cb
import preprocess as pp

# logs
LOG_PATH = "logs/"
LOG_INTERIM_PATH = f"{LOG_PATH}interim/"
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
PROCESSED_ENV_EXTRACTED_PATH = os.path.join(DATA_PATH,
                                            "processed/environment_statements/extracted/")
PROCESSED_ENV_PREPARED_PATH = os.path.join(DATA_PATH,
                                           "processed/environment_statements/prepared/")

REQUIRED_FOLDERS = [LOG_PATH,
                    f"{LOG_PATH}interim/",
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
DATA_EXTS = [".csv.gz", ".parquet"]
DATA_PPROCESS = "_ppreprocessed"

# logs and output files
# ---------------------
# ResearchGroups
sheet = SHEETS[5]
SHEET_RGROUPS = sheet
LOG_PPROC_RGROUPS = f"{sheet}{DATA_PPROCESS}{LOG_EXT}"

# ResearchDoctoralDegreesAwarded
sheet = SHEETS[2]
SHEET_DEGREES = sheet
LOG_PPROC_DEGREES = f"{sheet}{DATA_PPROCESS}{LOG_EXT}"

# ResearchIncome
sheet = SHEETS[3]
SHEET_INCOME = sheet
LOG_PPROC_INCOME = f"{sheet}{DATA_PPROCESS}{LOG_EXT}"

# ResearchIncomeInKind
sheet = SHEETS[4]
SHEET_INCOMEINKIND = sheet
LOG_PPROC_INCOMEINKIND = f"{sheet}{DATA_PPROCESS}{LOG_EXT}"

# Outputs
sheet = SHEETS[0]
SHEET_OUTPUTS = sheet
LOG_PPROC_OUTPUTS = f"{sheet}{DATA_PPROCESS}{LOG_EXT}"

# ImpactCaseStudies
sheet = SHEETS[1]
SHEET_IMPACTS = sheet
LOG_PPROC_IMPACTS = f"{sheet}{DATA_PPROCESS}{LOG_EXT}"

# Results
sheet = "Results"
SHEET_RESULTS = sheet
LOG_PPROC_RESULTS = f"{sheet}{DATA_PPROCESS}{LOG_EXT}"

# environment statements: institution
ENV_INSTITUTION = "institution"
LOG_PREPARE_ENV_INSTITUTION = f"{LOG_PREPARE}environment_institution{LOG_EXT}"
# DATA_PREPARE_ENV_INSTITUTION = f"{PROCESSED_ENV_PREPARED_PATH}"\
#                                f"EnvStatementsInstitutionLevel{DATA_EXT}"

# environment statements: unit
ENV_UNIT = "unit"
LOG_PREPARE_ENV_UNIT = f"{LOG_PREPARE}environment_unit{LOG_EXT}"
# DATA_PREPARE_ENV_UNIT = f"{PROCESSED_ENV_PREPARED_PATH}EnvStatementsUnitLevel{DATA_EXT}"


def extract_sheet(fpath, sname, header, index_col=None):
    """ Extract a sheet from an excel file and save it as csv file.

    Args:
        fpath (str): Filename of the Excel file.
        sname (str): Name of the sheet to extract from the Excel file.
        header (int): Row number to use as the column names.
        index_col (int): Column number to use as the row labels.
    """

    # read the excel file
    dobj = pd.ExcelFile(os.path.join(PROJECT_PATH, fpath))
    logging.info(f"{sname} - read sheet from '{fpath}'")

    # parse sheet
    dset = dobj.parse(sname,
                      header=header,
                      index_col=index_col
                      )
    logging.info(f"{sname} - parsed sheet: {dset.shape[0]} records")

    return dset


def export_sheet(dset, sname):

    for ext in DATA_EXTS:
        fname = os.path.join(PROCESSED_SHEETS_PATH, f"{sname}{DATA_PPROCESS}{ext}")
        if ext == ".csv.gz":
            dset.to_csv(os.path.join(PROJECT_PATH, fname),
                        index=True,
                        compression='gzip')
        elif ext == ".parquet":
            dset.to_parquet(os.path.join(PROJECT_PATH, fname),
                            index=True)
        logging.info(f"{sname} - write dataset to '{fname}'")


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
