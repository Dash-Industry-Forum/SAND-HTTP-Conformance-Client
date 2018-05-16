# SAND Conformance Client

[![Build Status](https://travis-ci.org/edrthomas/SAND-HTTP-Conformance-Client.svg?branch=master)](https://travis-ci.org/edrthomas/SAND-HTTP-Conformance-Client)

This implements a conformance client for ISO/IEC 23009-5 Server And Network-
asssited DASH (SAND).

It validates the incoming SAND messages as well as the protocols used by
the DANE.

## Requirements

- [pip](https://pip.pypa.io/en/stable/)

## Installation

```
pip install -r requirements.txt
```

## Usage

Help documentattion:

```
python sand_client.py --help
```

Outputs:

```
Usage: sand_client.py [OPTIONS]

  Execute the request and the validation of the received HTTP response.

Options:
  -u, --url_to_request TEXT       DANE URL to request, e.g. http://mydane.com
  -p, --protocol [assistance|enforcement|error]
                                  Protocols to carry PER messages specified in
                                  ISO/IEC 23009-5
  --help                          Show this message and exit.
```
