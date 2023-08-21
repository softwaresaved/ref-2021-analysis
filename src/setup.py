from io import StringIO
import sys
import os
import read_write as rw


def reset_folders():
    """ Reset the data folders.
    """
    # redirect stdout to a buffer
    buffer = StringIO()
    sys.stdout = buffer

    # reset folders
    rw.clean_folders()
    rw.create_folders()

    # restore stdout
    sys.stdout = sys.__stdout__

    fname = os.path.join(rw.LOG_PATH, 'setup.log')
    with open(os.path.join(rw.PROJECT_PATH, fname), 'w') as f:
        f.write(buffer.getvalue())
    print(f"Log saved in {fname}")


if __name__ == "__main__":
    reset_folders()
