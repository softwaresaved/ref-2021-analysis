from io import StringIO
import sys
import os
import read_write as rw


def main():
    text = "Started setting up"
    print(text)

    # redirect stdout to a buffer
    buffer = StringIO()
    sys.stdout = buffer

    # create folders
    rw.create_folders()

    # restore stdout
    sys.stdout = sys.__stdout__

    fname = os.path.join(rw.LOGS_PATH, 'setup_log.txt')
    with open(os.path.join(rw.PROJECT_PATH, fname), 'w') as f:
        f.write(buffer.getvalue())
    print(f"Log saved in {fname}")


if __name__ == "__main__":
    main()
