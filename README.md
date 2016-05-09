# SAND conformance client

This implements a conformance client for ISO/IEC 23009-5 Server And Network
asssited DASH (SAND).

It allows to send SAND messages according to the HTTP header protocol.

## Requirements

- None

## Installation

None required

## Usage

There are two possible forms of command:

```python sand_client_header.py <url> <header_name> <header_value>```

```python sand_client_header.py <url> <file_name>```

```<url>``` must be to an http server, but may be specified either as a full url
(```http://localhost:5000/headers```) or abbreviated with only the server and path
(```localhost:5000/header```)

Example:

```python sand_client_header.py localhost:5000/headers SAND-MaxRTT "maxRTT=200"```

For the version with ```<file_name>```, the file should contain one HTTP header per line.