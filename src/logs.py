""" Logging functions. """
import datetime


def print_tstamp(text):
    """ Print a timestamped message.

    Args:
        text (str): The message to print.
    """

    now = datetime.datetime.now()
    print(f"[{now.strftime('%Y-%m-%d %H:%M:%S')}] {text}")
