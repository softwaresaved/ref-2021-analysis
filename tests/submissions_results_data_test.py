""" This module tests the data in the processed submissions and results files. """
import os
from fastparquet import ParquetFile
import REF2021_processing.read_write as rw


def test_processed_submissions_records():
    """Test if the processed submissions files have the expected number of records."""

    source = "submissions"
    for sheet, sheet_name in rw.SOURCES[source]["sheets"].items():
        fpath = os.path.join(
            rw.PROJECT_PATH,
            f"{rw.SOURCES[source]['output_path']}{sheet_name}{rw.OUTPUT_EXTENSION}",
        )
        pf = ParquetFile(fpath)
        records = pf.count()
        expected_records = rw.SOURCES[source]["tests"][sheet]["records"]
        assert (
            records == expected_records
        ), f"{sheet_name}: {records} records, expected {expected_records}"


def test_processed_results_records():
    """Test if the processed results file has the expected number of records."""

    source = "results"
    sheet_name = rw.SOURCES[source]["sheet"]
    fpath = os.path.join(
        rw.PROJECT_PATH,
        f"{rw.SOURCES[source]['output_path']}{sheet_name}{rw.OUTPUT_EXTENSION}",
    )
    pf = ParquetFile(fpath)
    records = pf.count()
    expected_records = rw.SOURCES[source]["tests"]["records"]
    assert (
        records == expected_records
    ), f"{sheet_name}: {records} records, expected {expected_records}"


def test_processed_institution_environment_statements_records():
    """Test if the processed institution environment statements
    file has the expected number of records.
    """

    source = "environment_statements"
    level = "institution"
    level_name = rw.SOURCES[source][level]["name"]
    fpath = os.path.join(
        rw.PROJECT_PATH,
        f"{rw.SOURCES[source][level]['output_path']}{level_name}{rw.OUTPUT_EXTENSION}",
    )
    pf = ParquetFile(fpath)
    records = pf.count()
    expected_records = rw.SOURCES[source][level]["tests"]["records"]
    assert (
        records == expected_records
    ), f"{level_name}: {records} records, expected {expected_records}"


def test_processed_unit_environment_statements_records():
    """Test if the processed unit environment statements
    file has the expected number of records.
    """

    source = "environment_statements"
    level = "unit"
    level_name = rw.SOURCES[source][level]["name"]
    fpath = os.path.join(
        rw.PROJECT_PATH,
        f"{rw.SOURCES[source][level]['output_path']}{level_name}{rw.OUTPUT_EXTENSION}",
    )
    pf = ParquetFile(fpath)
    records = pf.count()
    expected_records = rw.SOURCES[source][level]["tests"]["records"]
    assert (
        records == expected_records
    ), f"{level_name}: {records} records, expected {expected_records}"
