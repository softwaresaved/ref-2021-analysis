import os

import pandas as pd
import logging

# logs
LOG_PATH = "logs/"
LOG_INTERIM_PATH = f"{LOG_PATH}interim/"
LOG_EXT = ".log"
LOG_UNZIP = os.path.join(LOG_PATH, f"unzip_environment_statements{LOG_EXT}")

# data paths
PROJECT_PATH = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
DATA_PATH = "data/"
RAW_PATH = os.path.join(DATA_PATH, "raw/")
RAW_ENV_PATH = os.path.join(RAW_PATH, "environment_statements/")
RAW_ENV_INST_PATH = os.path.join(RAW_ENV_PATH, "institution/")
RAW_ENV_UNIT_PATH = os.path.join(RAW_ENV_PATH, "unit/")
PROCESSED_SHEETS_PATH = os.path.join(DATA_PATH, "processed/sheets/")
PROCESSED_ENV_EXTRACTED_PATH = os.path.join(
    DATA_PATH, "processed/environment_statements/extracted/"
)
PROCESSED_ENV_PREPARED_PATH = os.path.join(
    DATA_PATH, "processed/environment_statements/prepared/"
)

# data files
RAW_SUBMISSIONS_FNAME = f"{RAW_PATH}REF-2021-Submissions-All-2022-07-27.xlsx"
RAW_SUBMISSIONS_HEADER_INDEX = 4
RAW_RESULTS_FNAME = f"{RAW_PATH}REF-2021-Results-All-2022-05-06.xlsx"
RAW_RESULTS_HEADER_INDEX = 6
ENV_FNAME = f"{RAW_PATH}REF-2021-EnvironmentStatements-Extract-2023-08-22.zip"
SHEETS = [
    "Outputs",
    "ImpactCaseStudies",
    "ResearchDoctoralDegreesAwarded",
    "ResearchIncome",
    "ResearchIncomeInKind",
    "ResearchGroups",
]
DATA_EXTS = [".parquet"]
PPROCESS = "_preprocessed"

# logs and output files
# ---------------------
# ResearchGroups
sheet = SHEETS[5]
SHEET_RGROUPS = sheet
LOG_PPROC_RGROUPS = f"{sheet}{PPROCESS}{LOG_EXT}"

# ResearchDoctoralDegreesAwarded
sheet = SHEETS[2]
SHEET_DEGREES = sheet
LOG_PPROC_DEGREES = f"{sheet}{PPROCESS}{LOG_EXT}"

# ResearchIncome
sheet = SHEETS[3]
SHEET_INCOME = sheet
LOG_PPROC_INCOME = f"{sheet}{PPROCESS}{LOG_EXT}"

# ResearchIncomeInKind
sheet = SHEETS[4]
SHEET_INCOMEINKIND = sheet
LOG_PPROC_INCOMEINKIND = f"{sheet}{PPROCESS}{LOG_EXT}"

# Outputs
sheet = SHEETS[0]
SHEET_OUTPUTS = sheet
LOG_PPROC_OUTPUTS = f"{sheet}{PPROCESS}{LOG_EXT}"

# ImpactCaseStudies
sheet = SHEETS[1]
SHEET_IMPACTS = sheet
LOG_PPROC_IMPACTS = f"{sheet}{PPROCESS}{LOG_EXT}"

# Results
sheet = "Results"
SHEET_RESULTS = sheet
LOG_PPROC_RESULTS = f"{sheet}{PPROCESS}{LOG_EXT}"

# environment statements: institution
ENV_INSTITUTION = "EnvironmentStatementsInstitutionLevel"
LOG_PPROC_ENV_INSTITUTION = f"{ENV_INSTITUTION}{PPROCESS}{LOG_EXT}"

# environment statements: unit
ENV_UNIT = "EnvironmentStatementsUnitLevel"
LOG_PPROC_ENV_UNIT = f"{ENV_UNIT}{PPROCESS}{LOG_EXT}"


def extract_sheet(fpath, sname, header, index_col=None):
    """Extract a sheet from an excel file and save it as csv file.

    Args:
        fpath (str): Filename of the Excel file.
        sname (str): Name of the sheet to extract from the Excel file.
        header (int): Row number to use as the column names.
        index_col (int): Column number to use as the row labels.

    Returns:
        dset (pandas.DataFrame): Extracted sheet.
    """

    # read the excel file
    dobj = pd.ExcelFile(os.path.join(PROJECT_PATH, fpath))
    logging.info(f"{sname} - read sheet from '{fpath}'")

    # parse sheet
    dset = dobj.parse(sname, header=header, index_col=index_col)
    logging.info(f"{sname} - parsed sheet: {dset.shape[0]} records")

    return dset


def export_dataframe(dset, fname_root, log_prefix):
    """Export a dataframe to csv or parquet file.

    Args:
        dset (pandas.DataFrame): Dataset to export.
        fname_root (str): Filename root.
        log_prefix (str): Prefix for log messages.
    """

    for ext in DATA_EXTS:
        fname = f"{fname_root}{ext}"
        if ext == ".csv.gz":
            dset.to_csv(
                os.path.join(PROJECT_PATH, fname), index=True, compression="gzip"
            )
        elif ext == ".parquet":
            dset.to_parquet(os.path.join(PROJECT_PATH, fname), index=True)
        logging.info(f"{log_prefix} - write dataset to '{fname}'")


def read_dataframe(fpath, log_prefix):
    """Read a dataframe from csv or parquet file.

    Args:
        fpath (str): Filename.
        log_prefix (str): Prefix for log messages.

    Returns:
        dset (pandas.DataFrame): Dataset.
    """

    ext = os.path.splitext(fpath)[1]
    if ext == ".csv.gz":
        dset = pd.read_csv(
            os.path.join(PROJECT_PATH, fpath), index=True, compression="gzip"
        )
    elif ext == ".parquet":
        dset = pd.read_parquet(os.path.join(PROJECT_PATH, fpath))
    logging.info(f"{log_prefix} - read dataset from '{fpath}'")

    return dset
