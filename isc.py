"""A Pythonic interface to the ISC/DShield API."""

import datetime
import requests

XML = "?xml"
JSON = "?json"
TEXT = "?text"
PHP = "?php"

__BASE_URL = "https://isc.sans.edu/api/"


class Error(Exception):
    """Base class for custom exceptions."""


def _strip_and_reformat(data):
    """Strip out 'METAKEYINFO', and reformat a dict into a list if it has keys
    like "0", "1", etc. Does not modify the `data` parameter.
    """
    data_copy = data.copy()
    try:
        data_copy.__delitem__('METAKEYINFO')
        return [data_copy[k] for k in sorted(data_copy, key=int)]
    except (KeyError, ValueError):
        return data_copy

def _get(function, output_format=None):
    """Get and return data from the API.

    :returns: A str, list, or dict, depending on the input values and API data.
    """
    if output_format:
        return requests.get(''.join([__BASE_URL, function, output_format])).text
    return _strip_and_reformat(requests.get(''.join([__BASE_URL, function, JSON])).json())


def backscatter(date=None, rows=None):
    """Returns possible backscatter data.

    This report only includes "syn ack" data and is summarized by source port.

    :date: optional string (in Y-M-D format) or datetime.date() object
    :rows: optional number of rows returned (default 1000)
    """
    uri = 'backscatter'
    if date:
        try:
            uri = '/'.join([uri, date.strftime("%Y-%m-%d")])
        except AttributeError:
            uri = '/'.join([uri, date])
    if rows:
        uri = '/'.join([uri, str(rows)])
    return _get(uri)
