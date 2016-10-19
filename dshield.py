"""A Pythonic interface to the Internet Storm Center / DShield API."""

import requests

__version__ = "0.2"

XML = "?xml"
JSON = "?json"
TEXT = "?text"
PHP = "?php"

__BASE_URL = "https://dshield.org/api/"


class Error(Exception):
    """Custom exception class."""


def _get(function, return_format=None):
    """Get and return data from the API.

    :returns: A str, list, or dict, depending on the input values and API data.
    """
    if return_format:
        return requests.get(''.join([__BASE_URL, function, return_format])).text
    return requests.get(''.join([__BASE_URL, function, JSON])).json()


def backscatter(date=None, rows=None, return_format=None):
    """Returns possible backscatter data.

    This report only includes "syn ack" data and is summarized by source port.

    :param date: optional string (in Y-M-D format) or datetime.date() object
    :param rows: optional number of rows returned (default 1000)
    :returns: list -- backscatter data.
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

    Count: (also reports or records) total number of packets blocked from
    this IP.
    Attacks: (also targets) number of unique destination IP addresses for
    these packets.

    :param ip_address: a valid IP address
    """
    response = _get('ip/{address}'.format(address=ip_address), return_format)
    if 'bad IP address' in str(response):
        raise Error('Bad IP address, {address}'.format(address=ip_address))
    else:
        return response

def port(port_number, return_format=None):
    """Summary information about a particular port.

    In the returned data:

    Records: Total number of records for a given date.
    Targets: Number of unique destination IP addresses.
    Sources: Number of unique originating IPs.

    :param port_number: a string or integer port number
    """
    response = _get('port/{number}'.format(number=port_number), return_format)
    if 'bad port number' in str(response):
        raise Error('Bad port number, {number}'.format(number=port_number))
    else:
        return response

def portdate(port_number, date=None, return_format=None):
    """Information about a particular port at a particular date.

    If the date is ommited, today's date is used.

    :param port_number: a string or integer port number
    :param date: an optional string in 'Y-M-D' format or datetime.date() object
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

def topports(sort_by=None, limit=None, date=None, return_format=None):
    """Information about top ports for a particular date with return limit.

    :param sort_by: one of 'records', 'targets', 'sources'
    :param limit: number of records to be returned
    :param date: an optional string in 'Y-M-D' format or datetime.date() object
    """
    uri = 'topports'
    if sort_by:
        uri = '/'.join([uri, sort_by])
        if limit:
            uri = '/'.join([uri, str(limit)])
            if date:
                try:
                    uri = '/'.join([uri, date.strftime("%Y-%m-%d")])
                except AttributeError:
                    uri = '/'.join([uri, date])
    return _get(uri, return_format)

def topips(sort_by=None, limit=None, date=None, return_format=None):
    """Information about top ports for a particular date with return limit.

    :param sort_by: one of 'records', 'attacks'
    :param limit: number of records to be returned
    :param date: an optional string in 'Y-M-D' format or datetime.date() object
    """
    uri = 'topips'
    if sort_by:
        uri = '/'.join([uri, sort_by])
        if limit:
            uri = '/'.join([uri, str(limit)])
            if date:
                try:
                    uri = '/'.join([uri, date.strftime("%Y-%m-%d")])
                except AttributeError:
                    uri = '/'.join([uri, date])
    return _get(uri, return_format)

def sources(sort_by=None, limit=None, date=None, return_format=None):
    """Information summary from the last 30 days about source IPs with return
    limit.

    :param sort_by: one of 'ip', 'count', 'attacks', 'firstseen', 'lastseen'
    :param limit: number of records to be returned (max 10000)
    :param date: an optional string in 'Y-M-D' format or datetime.date() object
    """
    uri = 'sources'
    if sort_by:
        uri = '/'.join([uri, sort_by])
        if limit:
            uri = '/'.join([uri, str(limit)])
            if date:
                try:
                    uri = '/'.join([uri, date.strftime("%Y-%m-%d")])
                except AttributeError:
                    uri = '/'.join([uri, date])
    return _get(uri, return_format)

def porthistory(port_number, start_date=None, end_date=None, return_format=None):
    """Returns port data for a range of dates.

    In the return data:

    Records: Total number of records for a given date range.
    Targets: Number of unique destination IP addresses.
    Sources: Number of unique originating IPs.

    :param port_number: a valid port number (required)
    :param start_date: string or datetime.date(), default is 30 days ago
    :param end_date: string or datetime.date(), default is today
    """
    uri = 'porthistory/{port}'.format(port=port_number)
    if start_date:
        try:
            uri = '/'.join([uri, start_date.strftime("%Y-%m-%d")])
        except AttributeError:
            uri = '/'.join([uri, start_date])
        if end_date:
            try:
                uri = '/'.join([uri, end_date.strftime("%Y-%m-%d")])
            except AttributeError:
                uri = '/'.join([uri, end_date])
    response = _get(uri, return_format)
    if 'bad port number' in str(response):
        raise Error('Bad port, {port}'.format(port=port_number))
    else:
        return response

def asnum(number, limit=None, return_format=None):
    """Returns a summary of the information our database holds for a
    particular ASNUM (similar to /asdetailsascii.html) with return limit.

    :param limit: number of records to be returned (max 2000)
    """
    uri = 'asnum/{number}'.format(number=number)
    if limit:
        uri = '/'.join([uri, str(limit)])
    return _get(uri, return_format)

def dailysummary(start_date=None, end_date=None, return_format=None):
    """Returns daily summary totals of targets, attacks and sources. Limit to
    30 days at a time. (Query 2002-01-01 to present)

    In the return data:

    Sources: Distinct source IP addresses the packets originate from.
    Targets: Distinct target IP addresses the packets were sent to.
    Reports: Number of packets reported.

    :param start_date: string or datetime.date(), default is today
    :param end_date: string or datetime.date(), default is today
    """
    uri = 'dailysummary'
    if start_date:
        try:
            uri = '/'.join([uri, start_date.strftime("%Y-%m-%d")])
        except AttributeError:
            uri = '/'.join([uri, start_date])
        if end_date:
            try:
                uri = '/'.join([uri, end_date.strftime("%Y-%m-%d")])
            except AttributeError:
                uri = '/'.join([uri, end_date])
    return _get(uri, return_format)

def daily404summary(date, return_format=None):
    """Returns daily summary information of submitted 404 Error Page
    Information.

    :param date: string or datetime.date() (required)
    """
    uri = 'daily404summary'
    if date:
        try:
            uri = '/'.join([uri, date.strftime("%Y-%m-%d")])
        except AttributeError:
            uri = '/'.join([uri, date])
    return _get(uri, return_format)

def daily404detail(date, limit=None, return_format=None):
    """Returns detail information of submitted 404 Error Page Information.

    :param date: string or datetime.date() (required)
    :param limit: string or int, limit for number of returned items
    """
    uri = 'daily404detail'
    if date:
        try:
            uri = '/'.join([uri, date.strftime("%Y-%m-%d")])
        except AttributeError:
            uri = '/'.join([uri, date])
        if limit:
            uri = '/'.join([uri, str(limit)])
    return _get(uri, return_format)

def glossary(term=None, return_format=None):
    """List of glossary terms and definitions.

    :param term: a whole or parital word to "search" in the API
    """
    uri = 'glossary'
    if term:
        uri = '/'.join([uri, term])
    return _get(uri, return_format)

def webhoneypotsummary(date, return_format=None):
    """API data for `Webhoneypot: Web Server Log Project
    <https://dshield.org/webhoneypot/>`_.

    :param date: string or datetime.date() (required)
    """
    uri = 'webhoneypotsummary'
    try:
        uri = '/'.join([uri, date.strftime("%Y-%m-%d")])
    except AttributeError:
        uri = '/'.join([uri, date])
    return _get(uri, return_format)

def webhoneypotbytype(date, return_format=None):
    """API data for `Webhoneypot: Attack By Type
    <https://isc.sans.edu/webhoneypot/types.html>`_. We currently use a set
    of regular expressions to determine the type of attack used to attack the
    honeypot. Output is the top 30 attacks for the last month.

    :param date: string or datetime.date() (required)
    """
    uri = 'webhoneypotbytype'
    try:
        uri = '/'.join([uri, date.strftime("%Y-%m-%d")])
    except AttributeError:
        uri = '/'.join([uri, date])
    return _get(uri, return_format)
