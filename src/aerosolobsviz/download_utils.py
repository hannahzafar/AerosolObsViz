#!/usr/bin/env python

import argparse
import datetime


def validate_date(date_string):
    """
    Validate date string format.

    Args:
        date_string: str
            Date string to validate

    Returns:
        str: Validated date string

    Raises:
        argparse.ArgumentTypeError : If date format is invalid
    """
    try:
        datetime.date.strptime(date_string, "%Y-%m-%d")
        return date_string
    except ValueError:
        raise argparse.ArgumentTypeError(
            f"Invalid date format: {date_string}. Use YYYY-MM-DD"
        )
