"""Tests for processed data and associated log files and folders."""
import os
import REF2021_processing.read_write as rw


def test_log_folder_exists():
    """Test if the log folder exists."""

    fpath = rw.LOGS["path"]
    assert os.path.exists(fpath), f"{fpath} does not exist"


def test_process_submissions_logs_exist():
    """Test if the logs files for submissions exist."""

    for sheet in rw.SOURCES["submissions"]["sheets"].values():
        fpath = f"{rw.LOGS['path']}{sheet}{rw.LOGS['extension']}"
        assert os.path.exists(fpath), f"{fpath} does not exist"
