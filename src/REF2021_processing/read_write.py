import os
import logging
import pandas as pd

import REF2021_processing.read_write as rw

PROJECT_PATH = os.path.dirname(os.path.abspath(__name__))

LOGS = {
    "path": "logs/",
    "interim_path": "logs/interim/",
    "extension": ".log",
}

SOURCES = {
    "submissions": {
        "raw_path": "data/raw/",
        "filename": "REF-2021-Submissions-All-2022-07-27.xlsx",
        "header_index": 4,
        "output_path": "data/processed/sheets/",
        "sheets": {
            "outputs": "Outputs",
            "impacts": "ImpactCaseStudies",
            "degrees": "ResearchDoctoralDegreesAwarded",
            "income": "ResearchIncome",
            "income_in_kind": "ResearchIncomeInKind",
            "groups": "ResearchGroups",
        },
    },
    "environment_statements": {
        "unit": {
            "extracted_path": "data/processed/environment_statements/extracted/unit/",
            "prefix": "Unit environment statement - ",
            "input_extension": ".txt",
            "name": "EnvironmentStatementsUnitLevel",
            "output_path": "data/processed/environment_statements/prepared/",
        },
        "institution": {
            "extracted_path": "data/processed/environment_statements/extracted/institution/",
            "name": "EnvironmentStatementsInstitutionLevel",
            "input_extension": ".txt",
            "prefix": "Institution environment statement - ",
            "output_path": "data/processed/environment_statements/prepared/",
        },
    },
    "results": {
        "raw_path": "data/raw/",
        "filename": "REF-2021-Results-All-2022-05-06.xlsx",
        "header_index": 6,
        "sheet": "Results",
    },
}

OUTPUT_EXTENSION = ".parquet"


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
    logging.info(f"{sname} - read sheet from '{relative_path(fpath)}'")

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

    fname = os.path.join(PROJECT_PATH, f"{fname_root}{OUTPUT_EXTENSION}")
    if OUTPUT_EXTENSION == ".csv.gz":
        dset.to_csv(fname, index=True, compression="gzip")
    elif OUTPUT_EXTENSION == ".parquet":
        dset.to_parquet(fname, index=True)
    logging.info(f"{log_prefix} - write dataset to '{relative_path(fname)}'")


def read_dataframe(fpath, log_prefix):
    """Read a dataframe from csv or parquet file.

    Args:
        fpath (str): Filename.
        log_prefix (str): Prefix for log messages.

    Returns:
        dset (pandas.DataFrame): Dataset.
    """

    ext = os.path.splitext(fpath)[1]
    fname = os.path.join(PROJECT_PATH, fpath)
    if ext == ".csv.gz":
        dset = pd.read_csv(fname, index=True, compression="gzip")
    elif ext == ".parquet":
        dset = pd.read_parquet(fname)
    logging.info(f"{log_prefix} - read dataset from '{fpath}'")

    return dset


def relative_path(fpath):
    """Return the relative path of a file.

    Args:
        fpath (str): File path.

    Returns:
        str: Relative path of the file.
    """

    return os.path.relpath(fpath, rw.PROJECT_PATH)


def rule_config(rule_name, config_name):
    """Return the configuration for a rule.

    Args:
        rule_name (str): Name of the rule.
        config_name (str): Name of the configuration.

    Returns:
        list or str: Configuration.
    """

    config = []
    logs_extension = LOGS["extension"]
    logs_path = LOGS["path"]

    if rule_name == "all":
        if config_name == "input":
            config = [
                # raw submissions
                os.path.join(
                    SOURCES["submissions"]["raw_path"],
                    SOURCES["submissions"]["filename"],
                ),
                # raw results
                os.path.join(
                    SOURCES["results"]["raw_path"], SOURCES["results"]["filename"]
                ),
            ]
            # extracted and processed sheets
            for source in SOURCES["submissions"]["sheets"].keys():
                config.append(
                    f"{logs_path}{SOURCES['submissions']['sheets'][source]}{logs_extension}"
                )
            # extracted and prepared environment statements
            for source in SOURCES["environment_statements"].keys():
                config.append(
                    f"{logs_path}{SOURCES['environment_statements'][source]['name']}"
                    f"{logs_extension}"
                )
            # extracted and prepared results
            log_fname = f"{SOURCES['results']['sheet']}{logs_extension}"
            config.append(os.path.join(logs_path, log_fname))
    elif rule_name in SOURCES["submissions"]["sheets"].keys():
        if config_name == "input":
            # raw submissions
            config = [
                os.path.join(
                    SOURCES["submissions"]["raw_path"],
                    SOURCES["submissions"]["filename"],
                )
            ]
        elif config_name == "output":
            log_fname = f"{SOURCES['submissions']['sheets'][rule_name]}{logs_extension}"
            config = os.path.join(logs_path, log_fname)
        elif config_name == "shell":
            config = f"python -m REF2021_processing.preprocess_sheet -s {rule_name}"
    elif rule_name in SOURCES["environment_statements"].keys():
        if config_name == "input":
            # raw submissions
            config = [
                os.path.join(
                    SOURCES["submissions"]["raw_path"],
                    SOURCES["submissions"]["filename"],
                )
            ]
        elif config_name == "output":
            log_fname = f"{SOURCES['environment_statements'][rule_name]['name']}{logs_extension}"
            config = os.path.join(logs_path, log_fname)
        elif config_name == "shell":
            config = (
                f"python -m REF2021_processing.prepare_envstatements -s {rule_name}"
            )
    elif rule_name == "results":
        if config_name == "input":
            # raw results
            config = [
                os.path.join(
                    SOURCES["results"]["raw_path"], SOURCES["results"]["filename"]
                )
            ]
            # extracted and prepared sheets
            for source in SOURCES["submissions"]["sheets"].keys():
                config.append(
                    f"{logs_path}{SOURCES['submissions']['sheets'][source]}{logs_extension}",
                )
            # extracted and prepared environment statements
            for source in SOURCES["environment_statements"].keys():
                config.append(
                    f"{logs_path}{SOURCES['environment_statements'][source]['name']}"
                    f"{logs_extension}"
                )
        elif config_name == "output":
            log_fname = f"{SOURCES['results']['sheet']}{logs_extension}"
            config = os.path.join(logs_path, log_fname)
        elif config_name == "shell":
            config = f"python -m REF2021_processing.preprocess_sheet -s {rule_name}"

    # make the paths absolute
    if config_name != "shell":
        if isinstance(config, list):
            config = [os.path.join(PROJECT_PATH, item) for item in config]
        elif isinstance(config, str):
            config = os.path.join(PROJECT_PATH, config)

    return config
