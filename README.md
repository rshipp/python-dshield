ISC
===

[![Build Status](https://travis-ci.org/rshipp/python-isc.svg)][travis]
[![Coverage Status](https://coveralls.io/repos/rshipp/python-isc/badge.png)][coveralls]
[![Code Health](https://landscape.io/github/rshipp/python-isc/master/landscape.png)][landscape]

A Python module to get data from the ISC/DShield [API][api].

[api]: https://isc.sans.edu/api/
[travis]: https://travis-ci.org/rshipp/python-isc
[coveralls]: https://coveralls.io/r/rshipp/python-isc
[landscape]: https://landscape.io/github/rshipp/python-isc/master

## Usage

Sphinx docs will be generated later. For now:

```python
import isc
isc.infocon()
# {'status': 'green'}
isc.infocon(isc.XML)
# '<?xml version="1.0" encoding="UTF-8"?>\n<infocon>\n<status>green</status>\n</infocon>'
```
