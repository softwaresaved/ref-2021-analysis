""" Prepares the extracted environment statements. """
import argparse
from io import StringIO
import sys
import os
import pandas as pd

import read_write as rw
import codebook as cb
import preprocess as pp
import logs as lg


def prepare_organization_statements():

    lg.print_tstamp("PPROC actions for organization envinroment statements")


def prepare_unit_statements():

    lg.print_tstamp("PPROC actions for unit envinroment statements")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prepares the extracted environment statements and saves it as csv file."
        )

    parser.add_argument("-e", "--envname",
                        required=True,
                        help="type of statements to prepare")

    args = parser.parse_args()
    ename = args.envname

    # redirect stdout to a buffer
    # ---------------------------
    buffer = StringIO()
    sys.stdout = buffer

    if ename == "organization":
        logfname = f"{rw.LOG_PREPARE_ENV_ORGANIZATION}" 
        prepare_organization_statements()
    elif ename == "unit":
        logfname = f"{rw.LOG_PREPARE_ENV_UNIT}" 
        prepare_unit_statements()

    # restore stdout
    # --------------
    sys.stdout = sys.__stdout__

    # save the log file
    # -----------------
    with open(os.path.join(rw.PROJECT_PATH, logfname), 'w') as f:
        f.write(buffer.getvalue())
