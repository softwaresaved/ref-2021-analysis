"""Tests for the read_write.py."""
import os
import REF2021_processing.read_write as rw


def test_logs_folder_and_files_exist():
    """Test if the logs folder and files exist."""

    # logs folder
    assert os.path.exists(rw.LOGS["path"])

    # logs files for sheets
    for sheet in rw.SOURCES["submissions"]["sheets"].values():
        assert os.path.exists(f"{rw.LOGS['path']}{sheet}{rw.LOGS['extension']}")

    # logs files for environment statements
    for statement in rw.SOURCES["environment_statements"].values():
        assert os.path.exists(
            f"{rw.LOGS['path']}{statement['name']}{rw.LOGS['extension']}"
        )

    # logs file for results
    assert os.path.exists(
        f"{rw.LOGS['path']}{rw.SOURCES['results']['sheet']}{rw.LOGS['extension']}"
    )
