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
SAND_METHOD_HEADER = "header"
SAND_METHOD_BODY = "body"

def validate_body(url):
    """
    Validate that the body of the HTTP response complies
    with the rules specified in ISO/IEX 23009-5.
    """
    is_valid = False
    try:
        message_resp = requests.get(url)

        if message_resp.headers["Content-Type"] != SAND_CONTENT_TYPE:
            logging.info(("[TEST] message KO|Wrong content type|"
                          "expected=%s|used=%s"),
                         SAND_CONTENT_TYPE,
                         message_resp.headers["Content-Type"])
        else:
            logging.info("[TEST] message OK|Valid content type|%s",
                         SAND_CONTENT_TYPE)

        validator = XMLValidator()
        try:
            if validator.from_string(message_resp.content):
                logging.info("[TEST] message OK|XML message format valid")
                is_valid = True
            else:
                logging.info("[TEST] message KO|XML message format invalid")
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
                is_valid = validate_body(sand_url)
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
@click.option("-m", "--sand_method", type=click.Choice([SAND_METHOD_HEADER,
                                                        SAND_METHOD_BODY]),
              help=("Location of the SAND informationin the HTTP response."))
def main(sand_method, url_to_request):
    """
    Execute the request and the validation of the received HTTP response.
    """
    success = False
    if sand_method == SAND_METHOD_HEADER:
        success = validate_header(url_to_request)

    elif sand_method == SAND_METHOD_BODY:
        success = validate_body(url_to_request)

    else:
        logging.error('Unknown SAND method "%s"', sand_method)
        return

    if success:
        logging.info("[RESULT] Success")
    else:
        logging.info("[RESULT] Failure")

    return success

if __name__ == "__main__":
    main()
