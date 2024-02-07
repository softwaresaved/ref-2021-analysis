""" This module tests the data in the processed submissions and results files. """
import os
from fastparquet import ParquetFile
import REF2021_processing.read_write as rw


def test_processed_submissions_record_numbers():
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


def test_processed_results_record_numbers():
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
