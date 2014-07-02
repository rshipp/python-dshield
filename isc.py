"""A Pythonic interface to the ISC/DShield API."""

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

def _get(function, output=None):
    """Get and return data from the API.

    :returns: A str, list, or dict, depending on the input values and API data.
    """
    if output:
        return requests.get(''.join([__BASE_URL, function, output])).text
    return _strip_and_reformat(requests.get(''.join([__BASE_URL, function, JSON])).json())
