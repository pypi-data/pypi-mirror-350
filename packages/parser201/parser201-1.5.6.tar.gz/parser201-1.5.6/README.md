![GitHub](https://img.shields.io/github/license/geozeke/parser201)
![PyPI](https://img.shields.io/pypi/v/parser201)
![PyPI - Status](https://img.shields.io/pypi/status/parser201)
![GitHub last commit](https://img.shields.io/github/last-commit/geozeke/parser201)
![GitHub issues](https://img.shields.io/github/issues/geozeke/parser201)
![PyPI - Downloads](https://img.shields.io/pypi/dm/parser201)
![GitHub repo size](https://img.shields.io/github/repo-size/geozeke/parser201)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/parser201)

<br>

<img
src="https://lh3.googleusercontent.com/d/1H04KVAA3ohH_dLXIrC0bXuJXDn3VutKc"
alt="Dinobox Logo" width="120"/>

## Features

The centerpiece of the parser201 module is the LogParser class. The
class initializer takes a single line from an Apache access log file and
extracts the individual fields into attributes within an object.

## Installation

```text
pip3 install parser201
```

## Usage

The most common use-case for parser201 is importing individual lines
from an Apache access log file and creating LogParser objects, like
this:

```python
from parser201 import LogParser

with open('access.log', 'r') as f:
    for line in f:
        lp = LogParser(line)
        # Use lp as desired: add to List, Dictionary, etc.
```

## Documentation

See: [parser201 Documentation][def].

[def]: https://geozeke.github.io/parser201
