"""A Pythonic interface to the ISC/DShield API."""

import requests

XML = "?xml"
JSON = "?json"
TEXT = "?text"
PHP = "?php"

__BASE_URL = "https://isc.sans.edu/api/"


class Error(Exception):
    """Base class for custom exceptions."""


def _get(function, output=None):
    """Get and return data from the API.

    :returns: A str, list, or dict, depending on the input values and API data.
    """
    if output:
        return requests.get(''.join([__BASE_URL, function, output])).text
    data = requests.get(''.join([__BASE_URL, function, JSON])).json()
    # Strip out 'METAKEYINFO', and reformat a dict into a list if it has keys
    # like "0", "1", etc.
    try:
        data.__delitem__('METAKEYINFO')
        return [data[k] for k in sorted(data, key=int)]
    except (KeyError, ValueError):
        return data
