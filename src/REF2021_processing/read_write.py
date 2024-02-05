import os
import logging
import pandas as pd

import REF2021_processing.read_write as rw

PROJECT_PATH = os.path.dirname(os.path.abspath(__name__))

paths = {
    "output_sheets": "data/processed/sheets/",
    "output_env": "data/processed/environment_statements/prepared/",
    "logs": "logs/",
    "logs_interim": "logs/interim/",
}

for key, value in paths.items():
    paths[key] = os.path.join(PROJECT_PATH, value)

sources = {
    "submissions": {
        "path": "data/raw/",
        "filename": "REF-2021-Submissions-All-2022-07-27.xlsx",
        "header_index": 4,
        "sheets": {
            "outputs": "Outputs",
            "impacts": "ImpactCaseStudies",
            "degrees": "ResearchDoctoralDegreesAwarded",
            "income": "ResearchIncome",
            "incomeinkind": "ResearchIncomeInKind",
            "groups": "ResearchGroups",
        },
    },
    "environment_statements": {
        "unit": {
            "path": "data/processed/environment_statements/extracted/unit/",
            "prefix": "Unit environment statement - ",
            "extension": ".txt",
            "name": "EnvironmentStatementsUnitLevel",
        },
        "institution": {
            "path": "data/processed/environment_statements/extracted/institution/",
            "name": "EnvironmentStatementsInstitutionLevel",
            "extension": ".txt",
            "prefix": "Institution environment statement - ",
        },
    },
    "results": {
        "path": "data/raw/",
        "filename": "REF-2021-Results-All-2022-05-06.xlsx",
        "header_index": 6,
        "sheet": "Results",
    },
}

extensions = {"logs": ".log", "outputs": [".parquet"]}


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

    for ext in rw.extensions["outputs"]:
        fname = os.path.join(PROJECT_PATH, f"{fname_root}{ext}")
        if ext == ".csv.gz":
            dset.to_csv(fname, index=True, compression="gzip")
        elif ext == ".parquet":
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
    config = []

    if rule_name == "all":
        if config_name == "input":
            config = [
                os.path.join(
                    PROJECT_PATH,
                    *[
                        sources["submissions"]["path"],
                        sources["submissions"]["filename"],
                    ],
                )
            ]
            for source in sources["submissions"]["sheets"].keys():
                config.append(
                    f"{paths['logs']}{sources['submissions']['sheets'][source]}{extensions['logs']}"
                )
            for source in sources["environment_statements"].keys():
                config.append(
                    f"{paths['logs']}{sources['environment_statements'][source]['name']}{extensions['logs']}"
                )
            log_fname = f"{sources['results']['sheet']}{extensions['logs']}"
            config.append([os.path.join(PROJECT_PATH, *[paths["logs"], log_fname])])
    elif rule_name in sources["submissions"]["sheets"].keys():
        if config_name == "input":
            config = [
                os.path.join(
                    PROJECT_PATH,
                    *[
                        sources["submissions"]["path"],
                        sources["submissions"]["filename"],
                    ],
                )
            ]
        elif config_name == "output":
            log_fname = (
                f"{sources['submissions']['sheets'][rule_name]}{extensions['logs']}"
            )
            config = [os.path.join(PROJECT_PATH, *[paths["logs"], log_fname])]
        elif config_name == "shell":
            config = f"python -m REF2021_processing.preprocess_sheet -s {rule_name}"
    elif rule_name in sources["environment_statements"].keys():
        if config_name == "input":
            config = [
                os.path.join(
                    PROJECT_PATH,
                    *[
                        sources["submissions"]["path"],
                        sources["submissions"]["filename"],
                    ],
                )
            ]
        elif config_name == "output":
            log_fname = f"{sources['environment_statements'][rule_name]['name']}{extensions['logs']}"
            config = [os.path.join(PROJECT_PATH, *[paths["logs"], log_fname])]
        elif config_name == "shell":
            config = (
                f"python -m REF2021_processing.prepare_envstatements -s {rule_name}"
            )
    elif rule_name == "results":
        if config_name == "input":
            config = [
                os.path.join(
                    PROJECT_PATH,
                    *[
                        sources["results"]["path"],
                        sources["results"]["filename"],
                    ],
                )
            ]
            for source in sources["submissions"]["sheets"].keys():
                config.append(
                    f"{paths['logs']}{sources['submissions']['sheets'][source]}{extensions['logs']}"
                )
            for source in sources["environment_statements"].keys():
                config.append(
                    f"{paths['logs']}{sources['environment_statements'][source]['name']}{extensions['logs']}"
                )
        elif config_name == "output":
            log_fname = f"{sources['results']['sheet']}{extensions['logs']}"
            config = [os.path.join(PROJECT_PATH, *[paths["logs"], log_fname])]
        elif config_name == "shell":
            config = f"python -m REF2021_processing.preprocess_sheet -s {rule_name}"

    return config
