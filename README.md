DShield
=======

[![Build Status](https://travis-ci.org/rshipp/python-dshield.svg)][travis]
[![Coverage Status](https://coveralls.io/repos/rshipp/python-dshield/badge.png)][coveralls]
[![Code Health](https://landscape.io/github/rshipp/python-dshield/master/landscape.png)][landscape]

A Python module to get data from the ISC/DShield [API][api].

[api]: https://dshield.org/api/
[travis]: https://travis-ci.org/rshipp/python-dshield
[coveralls]: https://coveralls.io/r/rshipp/python-dshield
[landscape]: https://landscape.io/github/rshipp/python-dshield/master

## Usage

Sphinx docs will be generated later. For now:

```python
import dshield
dshield.infocon()
# {'status': 'green'}
dshield.infocon(dshield.XML)
# '<?xml version="1.0" encoding="UTF-8"?>\n<infocon>\n<status>green</status>\n</infocon>'
```
