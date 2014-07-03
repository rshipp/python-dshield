"""A Pythonic interface to the ISC/DShield API."""

import requests

XML = "?xml"
JSON = "?json"
TEXT = "?text"
PHP = "?php"

__BASE_URL = "https://dshield.org/api/"


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

def _get(function, return_format=None):
    """Get and return data from the API.

    :returns: A str, list, or dict, depending on the input values and API data.
    """
    if return_format:
        return requests.get(''.join([__BASE_URL, function, return_format])).text
    return _strip_and_reformat(requests.get(''.join([__BASE_URL, function, JSON])).json())


def backscatter(date=None, rows=None, return_format=None):
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
    return _get(uri, return_format)

def handler(return_format=None):
    """Returns the name of the handler of the day."""
    return _get('handler', return_format)

def infocon(return_format=None):
    """Returns the current infocon level (green, yellow, orange, red)."""
    return _get('infocon', return_format)

def ip(ip_address, return_format=None):
    """Returns a summary of the information our database holds for a
    particular IP address (similar to /ipinfo.html).

    In the returned data:
    Count - (also reports or records) total number of packets blocked from
    this IP.
    Attacks - (also targets) number of unique destination IP addresses for
    these packets.

    :ip_address: a valid IP address
    """
    response = _get('ip/{address}'.format(address=ip_address), return_format)
    if 'bad IP address' in str(response):
        raise Error('Bad IP address, {address}'.format(address=ip_address))
    else:
        return response

def port(port_number, return_format=None):
    """Summary information about a particular port.

    In the returned data:
    Records - Total number of records for a given date.
    Targets - Number of unique destination IP addresses.
    Sources - Number of unique originating IPs.

    :port_number: a string or integer port number
    """
    response = _get('port/{number}'.format(number=port_number), return_format)
    if 'bad port number' in str(response):
        raise Error('Bad port number, {number}'.format(number=port_number))
    else:
        return response

def portdate(port_number, date=None, return_format=None):
    """Information about a particular port at a particular date.

    If the date is ommited, today's date is used.

    :port_number: a string or integer port number
    :date: an optional string or datetime.date() object
    """
    uri = 'portdate/{number}'.format(number=port_number)
    if date:
        try:
            uri = '/'.join([uri, date.strftime("%Y-%m-%d")])
        except AttributeError:
            uri = '/'.join([uri, date])
    response = _get(uri, return_format)
    if 'bad port number' in str(response):
        raise Error('Bad port number, {number}'.format(number=port_number))
    else:
        return response
