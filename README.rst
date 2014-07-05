DShield
=======

.. image:: https://travis-ci.org/rshipp/python-dshield.svg?branch=master
   :target: https://travis-ci.org/rshipp/python-dshield
   :alt: Build Status
.. image:: https://coveralls.io/repos/rshipp/python-dshield/badge.png?branch=master
   :target: https://coveralls.io/r/rshipp/python-dshield?branch=master 
   :alt: Test Coverage
.. image:: https://landscape.io/github/rshipp/python-dshield/master/landscape.png
   :target: https://landscape.io/github/rshipp/python-dshield/master
   :alt: Code Health

A Pythonic interface to the Internet Storm Center / DShield API_.

Usage
-----

For the full documentation, see the ReadTheDocs_ site. If you just
want a quick start::

    >>> import dshield
    >>> dshield.infocon()
    {'status': 'green'}
    >>> dshield.infocon(dshield.XML)
    '<?xml version="1.0" encoding="UTF-8"?>\n<infocon>\n<status>green</status>\n</infocon>'

.. _API: https://dshield.org/api/
.. _ReadTheDocs: http://dshield.readthedocs.org/en/latest/
