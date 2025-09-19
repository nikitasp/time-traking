import argparse
from datetime import datetime, timedelta

def validate_date(date_string):
    """
    Custom type function for argparse to validate and convert a date string.
    Expected format: YYYY-MM-DD
    """
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid date format: '{date_string}'. Expected YYYY-MM-DD")