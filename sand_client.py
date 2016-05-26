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

import sys
import logging
import urllib
import requests

from sand.xml_message import XMLValidator


root = logging.getLogger()
root.setLevel(logging.DEBUG)

# HTTP headers are case insensitive, we use lower case
SAND_HEADER = "mpeg-dash-sand"
# SAND content type
SAND_CONTENT_TYPE = "application/sand+xml"
# Method 
SAND_METHOD_HEADER= "header"
SAND_METHOD_BODY = "body"
        
def validate_body(url):
    is_valid = False
    try:
        message_request = requests.get(url)

        if message_request.headers["Content-Type"] != SAND_CONTENT_TYPE:
            logging.error(("TEST message KO|Wrong content type|" +
                           "expected=%s|used=%s"), 
                           SAND_CONTENT_TYPE,
                           message_request.headers["Content-Type"])
        else:
            logging.info("TEST message OK|Valid content type|%s",
                         SAND_CONTENT_TYPE)
        
        validator = XMLValidator()
        try:
            if validator.from_string(message_request.content):
                logging.info("TEST message OK|XML message format valid")
                is_valid = True
            else:
                logging.error("TEST message KO|XML message format invalid")
        except:
            logging.error("TEST message KO|XML message format invalid")

    except requests.exceptions.RequestException as e:
        logging.error("TEST message KO|Could not retrieve the message|%s",
                      url)
        logging.error(e)
   
    return is_valid

def validate_header(url):
    is_valid = False
    r = requests.get(url)

    # Test 1 : Presence of MPEG DASH SAND header in response
    if SAND_HEADER in r.headers:
        logging.info("TEST header OK|%s header found in the response",
                      SAND_HEADER)
        sand_url = r.headers[SAND_HEADER]

        # Test 2 : Check the content of the header is a valid URL
        try:
            urllib.urlopen(sand_url)
            logging.info("TEST URL OK|The provided URL is valid|%s",
                         sand_url)

        except IOError:
            logging.error("TEST URL KO|The provided URL is not valid|%s",
                          sand_url)

        # Test 3 : Validating the provided message
        is_valid = validate_body(sand_url)

    else:
        logging.error("TEST header KO|No %s header found in the response.",
                      SAND_HEADER)
    return is_valid

def print_help():
    print "usage sand_client.py SAND_METHOD URL_TO_REQUEST"
    print ""
    print "SAND_METHOD=header|body"
    print ""

def main():
    sand_method = sys.argv[1]
    url_to_request = sys.argv[2]

    if sand_method == SAND_METHOD_HEADER:
        return validate_header(url_to_request)

    elif sand_method == SAND_METHOD_BODY:
        return validate_body(url_to_request)

    else:
        print_help()
        logging.error('Unknown SAND method "%s"', sand_method)

if __name__ == "__main__":
    main()
