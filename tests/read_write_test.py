"""Tests for the read_write.py."""
import os
import REF2021_processing.read_write as rw


def test_folders_files_exist():

    # check if the logs and data folders exist
    assert os.path.exists(rw.paths["logs"])



