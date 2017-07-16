#!/usr/bin/python

"""
SAND conformance server.

This implements a conformance server for ISO/IEC 23009-5 SAND.
It validates the incoming SAND messages as well as the protocols used by
a SAND client.

Copyright (c) 2016-, ISO/IEC JTC1/SC29/WG11
All rights reserved.

See AUTHORS for a full list of authors.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
* Redistributions of source code must retain the above copyright
notice, this list of conditions and the following disclaimer.
* Redistributions in binary form must reproduce the above copyright
notice, this list of conditions and the following disclaimer in the
documentation and/or other materials provided with the distribution.
* Neither the name of the ISO/IEC nor the
names of its contributors may be used to endorse or promote products
derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDERS BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import logging
import re
import urllib
import requests
import click

from sand.xml_message import XMLValidator


logging.getLogger().setLevel(logging.DEBUG)

# HTTP headers are case insensitive, we use lower case
SAND_HEADER = "mpeg-dash-sand"

# SAND content type
SAND_CONTENT_TYPE = "application/sand+xml"

# Method
SAND_PER_PROTOCOL_ERROR = "error"
SAND_PER_PROTOCOL_ENFORCEMENT = "enforcement"
SAND_PER_PROTOCOL_ASSISTANCE = "assistance"

def validate_response(url, regex_status_code):
    """
    Validate that the body of the HTTP response complies
    with the rules specified in ISO/IEX 23009-5.
    """
    is_valid = True
    try:
        resp = requests.get(url)

        # Test 1 - Verify that the SAND mime type is used.
        if resp.headers["Content-Type"] != SAND_CONTENT_TYPE:
            logging.info(("[TEST] content_type header|KO|Wrong content type|"
                          "expected=%s|used=%s"),
                         SAND_CONTENT_TYPE,
                         resp.headers["Content-Type"])
            is_valid = False
        else:
            logging.info("[TEST] content-type header|OK|Valid content type|%s",
                         SAND_CONTENT_TYPE)

        # Test 2 - Verify that the HTTP response code is as expected.
        expected = re.compile(regex_status_code)
        if expected.match(str(resp.status_code)):
            logging.info("[TEST] HTTP response code|OK|value=%s",
                         resp.status_code)
        else:
            logging.info("[TEST] HTTP response code|KO|value=%s|regex=%s",
                         resp.status_code, regex_status_code)
            is_valid = False

        # Test 3 - Validate the SAND message in response.
        validator = XMLValidator()
        try:
            if validator.from_string(resp.content):
                logging.info("[TEST] message|OK|XML message format valid")
            else:
                logging.info("[TEST] message|KO|XML message format invalid")
                is_valid = False
        except:
            logging.error("XML message format invalid")

    except requests.exceptions.RequestException as error:
        logging.error("Could not retrieve the message|%s",
                      url)
        logging.error(error)
    except IOError as error:
        logging.error("Error when retrieving the message|%s",
                      url)
        logging.error(error)

    return is_valid

def validate_header(url):
    """
    Validate that the HTTP reoponse header complies with the conformance
    rules specified in ISO/IEC 23009-5.
    """
    is_valid = False
    try:
        response = requests.get(url)

        # Test 1 : Presence of MPEG DASH SAND header in response
        if SAND_HEADER in response.headers:
            logging.info("[TEST] header OK|%s header found in the response",
                         SAND_HEADER)
            sand_url = response.headers[SAND_HEADER]

            # Test 2 : Check the content of the header is a valid URL
            try:
                urllib.urlopen(sand_url)
                logging.info("[TEST] URL OK|The provided URL is valid|%s",
                             sand_url)

                # Test 3 : Validating the provided message
                is_valid = validate_response(sand_url, "200")
            except IOError:
                logging.info("[TEST] URL KO|The provided URL is not valid|%s",
                             sand_url)

        else:
            logging.info("[TEST] header KO|No %s header found in the response.",
                         SAND_HEADER)
    except requests.exceptions.RequestException as error:
        logging.error("Could not retrieve the message|%s",
                      url)
        logging.error(error)

    return is_valid

@click.command()
@click.option("-u", "--url_to_request", help=("DANE URL to request,"
                                              " e.g. http://mydane.com"))
@click.option("-p", "--protocol",
              type=click.Choice([SAND_PER_PROTOCOL_ASSISTANCE,
                                 SAND_PER_PROTOCOL_ENFORCEMENT,
                                 SAND_PER_PROTOCOL_ERROR]),
              help=("Protocols to carry PER messages"
                    " specified in ISO/IEC 23009-5"))
def run(protocol, url_to_request):
    """
    Execute the request and the validation of the received HTTP response.
    """
    success = False
    if protocol == SAND_PER_PROTOCOL_ASSISTANCE:
        success = validate_header(url_to_request)

    elif protocol == SAND_PER_PROTOCOL_ENFORCEMENT:
        success = validate_response(url_to_request, "300")

    elif protocol == SAND_PER_PROTOCOL_ERROR:
        success = validate_response(url_to_request, "4[0-9]{2}")

    else:
        logging.error('Unknown SAND PER protocol "%s"', protocol)
        return

    if success:
        logging.info("[RESULT] Success")
    else:
        logging.info("[RESULT] Failure")

    return success

if __name__ == "__main__":
    run()
