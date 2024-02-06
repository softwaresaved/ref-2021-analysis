""" Module to read and write data. """
import os
import logging
import pandas as pd


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
        "output_path": "data/processed/sheets/"
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
    logging.info("%s - read sheet from '%s'", sname, relative_path(fpath))

    # parse sheet
    dset = dobj.parse(sname, header=header, index_col=index_col)
    logging.info("%s - parsed sheet: %d records", sname, dset.shape[0])

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
    logging.info("%s - write dataset to '%s'", log_prefix, relative_path(fname))


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
    logging.info("%s - read dataset from '%s'", log_prefix, fpath)

    return dset


def relative_path(fpath):
    """Return the relative path of a file.

    Args:
        fpath (str): File path.

    Returns:
        str: Relative path of the file.
    """

    return os.path.relpath(fpath, PROJECT_PATH)


def rule_all():
    """Return the configuration for the rule all.

    Returns:
        list: Input files for rule all.
    """

    logs_extension = LOGS["extension"]
    logs_path = LOGS["path"]

    config = [
        # raw submissions
        os.path.join(
            SOURCES["submissions"]["raw_path"],
            SOURCES["submissions"]["filename"],
        ),
        # raw results
        os.path.join(SOURCES["results"]["raw_path"], SOURCES["results"]["filename"]),
    ]
    # extracted and processed sheets
    for source, _ in SOURCES["submissions"]["sheets"].items():
        config.append(
            f"{logs_path}{SOURCES['submissions']['sheets'][source]}{logs_extension}"
        )
    # extracted and prepared environment statements
    for source, _ in SOURCES["environment_statements"].items():
        config.append(
            f"{logs_path}{SOURCES['environment_statements'][source]['name']}"
            f"{logs_extension}"
        )
    # extracted and prepared results
    log_fname = f"{SOURCES['results']['sheet']}{logs_extension}"
    config.append(os.path.join(logs_path, log_fname))

    return relative_to_absolute_path(config)


def rule_submission_sheet(rule_name, config_name):
    """Return the configuration for a submission sheet rule.

    Args:
        rule_name (str): Name of the rule.
        config_name (str): Name of the configuration.

    Returns:
        list or str: rule configuration.
    """

    logs_extension = LOGS["extension"]
    logs_path = LOGS["path"]

    if config_name == "input":
        # raw submissions
        config = relative_to_absolute_path(
            [
                os.path.join(
                    SOURCES["submissions"]["raw_path"],
                    SOURCES["submissions"]["filename"],
                )
            ]
        )

    if config_name == "output":
        log_fname = f"{SOURCES['submissions']['sheets'][rule_name]}{logs_extension}"
        config = relative_to_absolute_path(os.path.join(logs_path, log_fname))

    if config_name == "shell":
        config = f"python -m REF2021_processing.process_submissions_and_results -s {rule_name}"

    return config


def rule_envstatements(rule_name, config_name):
    """Return the configuration for an environment statements rule.

    Args:
        rule_name (str): Name of the rule.
        config_name (str): Name of the configuration.

    Returns:
        list or str: rule configuration.
    """

    logs_extension = LOGS["extension"]
    logs_path = LOGS["path"]

    if config_name == "input":
        # raw submissions
        config = relative_to_absolute_path(
            [
                os.path.join(
                    SOURCES["submissions"]["raw_path"],
                    SOURCES["submissions"]["filename"],
                )
            ]
        )

    if config_name == "output":
        log_fname = (
            f"{SOURCES['environment_statements'][rule_name]['name']}{logs_extension}"
        )
        config = relative_to_absolute_path(os.path.join(logs_path, log_fname))

    if config_name == "shell":
        config = f"python -m REF2021_processing.process_envstatements -s {rule_name}"

    return config


def rule_results(config_name):
    """Return the configuration for the rule results.

    Args:
        config_name (str): Name of the configuration.

    Returns:
        list or str: rule configuration.
    """

    rule_name = "results"
    logs_extension = LOGS["extension"]
    logs_path = LOGS["path"]

    if config_name == "input":
        # raw results
        config = [
            os.path.join(SOURCES["results"]["raw_path"], SOURCES["results"]["filename"])
        ]
        # extracted and prepared sheets
        for source, _ in SOURCES["submissions"]["sheets"].items():
            config.append(
                f"{logs_path}{SOURCES['submissions']['sheets'][source]}{logs_extension}",
            )
        # extracted and prepared environment statements
        for source, _ in SOURCES["environment_statements"].items():
            config.append(
                f"{logs_path}{SOURCES['environment_statements'][source]['name']}"
                f"{logs_extension}"
            )
        config = relative_to_absolute_path(config)

    if config_name == "output":
        log_fname = f"{SOURCES['results']['sheet']}{logs_extension}"
        config = relative_to_absolute_path(os.path.join(logs_path, log_fname))

    if config_name == "shell":
        config = f"python -m REF2021_processing.process_submissions_and_results -s {rule_name}"

    return config


def relative_to_absolute_path(fpath):
    """Return the absolute path of a file.

    Args:
        fpath (str): File path.

    Returns:
        str: Absolute path of the file.
    """

    if isinstance(fpath, list):
        fpath_absolute = [os.path.join(PROJECT_PATH, item) for item in fpath]
    if isinstance(fpath, str):
        fpath_absolute = os.path.join(PROJECT_PATH, fpath)

    return fpath_absolute
