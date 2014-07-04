.. DShield documentation master file

DShield documentation
=====================

.. automodule:: dshield

.. toctree::
   :maxdepth: 2

   index

Return Format
-------------

Just like the DShield API itself, all functions in this library are able to
return data in a variety of formats. By default, the library will convert
data returned from the API to a native object, either a `dict` or a `list`
depending on the function. You can change this behavior by specifying the
`return_format` when calling a function. Valid values for the
`return_format` parameter are: `dshield.XML`, `dshield.JSON`,
`dshield.TEXT`, and `dshield.PHP`. When any of these formats are used,
the function will return a string containing the raw data from the API.

To give a simple example:

    >>> import dshield
    >>> dshield.infocon()
    {'status': 'green'}
    >>> dshield.infocon(dshield.JSON)
    '{"status":"green"}'


Functions
---------

The docstrings for these functions are for the most part taken directly
from the official API documentation_.

.. autofunction:: dshield.backscatter

.. autofunction:: dshield.handler
.. autofunction:: dshield.infocon
.. autofunction:: dshield.ip
.. autofunction:: dshield.port
.. autofunction:: dshield.portdate
.. autofunction:: dshield.topports
.. autofunction:: dshield.topips


Exceptions
----------

.. autoclass:: dshield.Error


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

.. _documentation: https://isc.sans.edu/api/
