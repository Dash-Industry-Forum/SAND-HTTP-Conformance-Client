#!/usr/bin/python

"""
SAND conformance client sending header messages.

This implements a conformance client for ISO/IEC 23009-5 SAND.
It sends HTTP GET requests containing SAND messages transported as HTTP headers.

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

import httplib, urllib

def check_header(server, path, name, value):
    headers = { name: value }
    conn = httplib.HTTPConnection(server)
    conn.request("GET", path, '', headers)
    response = conn.getresponse()
    print response.status, response.reason
    data = response.read()
    print data
    conn.close()

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 2:
        s_p = sys.argv[1]
        if s_p.startswith('http://'):
            s_p = s_p[7:]
        server, path = s_p.split('/', 1)
        path = '/' + path
    if len(sys.argv) == 4:
        check_header(server, path, sys.argv[2], sys.argv[3])
    elif len(sys.argv) == 3:
        with open(sys.argv[2]) as f:
            for line in f.readlines():
                if line.strip(): # ignore empty lines
                    h, v = line.split(':', 1)
                    check_header(server, path, h.strip(), v.strip())
    else:
        print '''Usage:
    %s <url> <header_name> <header_value>
    %s <url> <file_name>
<url> must be with protocol http, but may be abbreviated into <server>[:<port>]/<path>
Example: %s localhost:5000/headers SAND-MaxRTT "maxRTT=200"
For the form with <file_name>, file should contain headers to send, one per line.
''' % (sys.argv[0], sys.argv[0], sys.argv[0])

