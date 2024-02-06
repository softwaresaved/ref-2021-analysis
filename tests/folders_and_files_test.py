"""Tests for processed data and associated log files and folders."""
import os
import REF2021_processing.read_write as rw


# Submissions
# ===========
def test_process_submissions_logs_exist():
    """Test if the logs files for submissions exist."""

    for sheet in rw.SOURCES["submissions"]["sheets"].values():
        fpath = f"{rw.LOGS['path']}{sheet}{rw.LOGS['extension']}"
        assert os.path.exists(fpath), f"{fpath} does not exist"


def test_process_submissions_logs_empty():
    """Test if the logs files for submissions are empty."""

    for sheet in rw.SOURCES["submissions"]["sheets"].values():
        fpath = f"{rw.LOGS['path']}{sheet}{rw.LOGS['extension']}"
        assert not os.path.getsize(fpath) == 0, f"{fpath} is empty"


def test_process_submissions_output_exist():
    """Test if the processed files for submissions exist."""

    for sheet in rw.SOURCES["submissions"]["sheets"].values():
        fpath = (
            f"{rw.SOURCES['submissions']['output_path']}{sheet}{rw.OUTPUT_EXTENSION}"
        )
        assert os.path.exists(fpath), f"{fpath} does not exist"


def test_process_submissions_output_empty():
    """Test if the processed files for submissions are empty."""

    for sheet in rw.SOURCES["submissions"]["sheets"].values():
        fpath = (
            f"{rw.SOURCES['submissions']['output_path']}{sheet}{rw.OUTPUT_EXTENSION}"
        )
        assert not os.path.getsize(fpath) == 0, f"{fpath} is empty"


# Results
# =======
# Results logs
def test_process_results_logs_exist():
    """Test if the logs files for results exist."""

    sheet = rw.SOURCES["results"]["sheet"]
    fpath = f"{rw.LOGS['path']}{sheet}{rw.LOGS['extension']}"
    assert os.path.exists(fpath), f"{fpath} does not exist"


def test_process_results_logs_empty():
    """Test if the logs files for results are empty."""

    sheet = rw.SOURCES["results"]["sheet"]
    fpath = f"{rw.LOGS['path']}{sheet}{rw.LOGS['extension']}"
    assert not os.path.getsize(fpath) == 0, f"{fpath} is empty"


# Results output
def test_process_results_output_exist():
    """Test if the processed files for results exist."""

    fpath = (
        f"{rw.SOURCES['results']['output_path']}"
        f"{rw.SOURCES['results']['sheet']}{rw.OUTPUT_EXTENSION}"
    )
    assert os.path.exists(fpath), f"{fpath} does not exist"


def test_process_results_output_empty():
    """Test if the processed files for results are empty."""

    fpath = (
        f"{rw.SOURCES['results']['output_path']}"
        f"{rw.SOURCES['results']['sheet']}{rw.OUTPUT_EXTENSION}"
    )
    assert not os.path.getsize(fpath) == 0, f"{fpath} is empty"


# Environment statements
# =======================
def test_process_environment_statements_logs_exist():
    """Test if the logs files for environment statements exist."""

    for _, config in rw.SOURCES["environment_statements"].items():
        fpath = f"{rw.LOGS['path']}{config['name']}{rw.LOGS['extension']}"
        assert os.path.exists(fpath), f"{fpath} does not exist"


def test_process_environment_statements_logs_empty():
    """Test if the logs files for environment statements are empty."""

    for _, config in rw.SOURCES["environment_statements"].items():
        fpath = f"{rw.LOGS['path']}{config['name']}{rw.LOGS['extension']}"
        assert not os.path.getsize(fpath) == 0, f"{fpath} is empty"
