# SAND Conformance Client

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
  -m, --sand_method [header|body]
                                  Location of the SAND informationin the HTTP
                                  response.
  --help                          Show this message and exit.
```
