#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# file: asciidoc_http_server.py
#
# Copyright 2013 Frans Fuerst
#
# This code is likely to be licenced under Apache 2.0 or BSD licence plus
# a CLA will be needed. This CLA will make you keep all your rights on
# contributed code and enable the original project owner (me) to fork this
# project with all contributions under a different licence while the original
# code stays open.

"""run a http server which shows asciidoc files within a folder and compiles
   and returns asciidoc content of a file on click
"""

import optparse
import BaseHTTPServer
import SocketServer
import logging
import sys
import socket
import os
import subprocess

class ServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """acts like SimpleHTTPServer with the difference that it only shows
       asciidoc files and returns them as compiled asciidoc html code
    """

    def __init__(self, eins, zwei, drei):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, eins, zwei, drei)

        # should avoid socket.error "address already in use" but has no effect
        self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def do_HEAD(self):
        """returns the http header"""

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        """returns the http content
           we use subprocessing here rather than just importing content_generator
           because we want to be able to change content_generator without the
           need to restart the http server
        """

        _command  = [sys.executable]
        _command += [os.path.join(
            os.path.dirname(__file__),
            "content_generator.py") ]
        _command += ['-r', self.server.root]
        _command += ['-f', self.path]
        _command += ['-a', self.server.asciidoc_processor]
        _command += ['-s', self.server.asciidoc_suffix]

        _process = subprocess.Popen(args=_command, stdout=subprocess.PIPE)
        _stdout, _stderr = _process.communicate()
        _return = _process.returncode
        
        if _return == -2:
            sys.exit(0)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.wfile.write(_stdout)


        """
    def do_GET(self):
        #logging.error(self.headers)
        #print "HEADERS:", self.headers
        #print "DIR:", dir( self.headers )
        #print "KEYS:", self.headers.keys()
        #for k in self.headers.keys():
        #    print k, ":", self.headers[k]
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        #print
        #print
        client, port = self.client_address
        if "x-forwarded-for" in self.headers:
            #print "FORWARDED"
            client = self.headers["x-forwarded-for"]
        #print "client_address:", self.client_address
        #print "address_string:", self.address_string
        #print "command:", self.command
        #print "CLIENT:", client
        #print "path:", self.path
        if self.path == "/index.html" or self.path == "/" or self.path == "":
            log_str = "from %s at %d hostnames %s" % ( client, time.time(),
            socket.gethostbyaddr( client ) )
            print log_str
            open( "connections.log", "a" ).write( log_str + "\n" )
        return "hallo"

    def do_POST(self):
        logging.error(self.headers)
        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })
        for item in form.list:
            logging.error(item)
        SimpleHTTPServer.SimpleHTTPRequestHandler.do_GET(self)
        """

def main():
    """decouples from global space parses command lines arguments and
       starts the server
    """

    parser = optparse.OptionParser()

    parser.add_option("-r", "--root", dest = "root", default = ".",
                      help = "asciidoc document folder", metavar = "path")

    parser.add_option("-p", "--port", dest = "port", default = 8000,
                      help = "port used for http", metavar = "port-nr")

    parser.add_option("-a", "--asciidoc-path", dest = "asciidoc_path",
                      default = "asciidoc", help = "path to asciidoc",
                      metavar = "path")

    parser.add_option("-s", "--asciidoc-suffix", dest  = "asciidoc_suffix",
                      default = ".asciidoc.txt", help = "asciidoc file suffix")

    (options, args) = parser.parse_args()
    if len(args) > 0:
        parser.print_help()
        parser.error("unrecognized extra arguments %s\n"
                     "maybe you forgot an argument prefix?" % str(args))

    if hasattr(socket, 'setdefaulttimeout'):
        socket.setdefaulttimeout(2)

    port = int(options.port)
    logging.info( "serving at port %d", port)
    logging.info( "serving folder  '%s'", os.path.abspath(options.root))

    try:
        httpd = SocketServer.TCPServer(("", port), ServerHandler)
    except socket.error, ex:
        logging.error("could not create TCPServer: '%s'", ex)
        sys.exit( -1 )

    except Exception, ex:
        logging.error("something happened I did not think about yet: '%s'", ex)

    # bad: refactor
    httpd.root = options.root
    httpd.asciidoc_processor = options.asciidoc_path
    httpd.asciidoc_suffix = options.asciidoc_suffix

    httpd.serve_forever()

if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s %(levelname)s %(message)s',
        datefmt="%y%m%d-%H%M%S",
        level=logging.DEBUG)

    logging.addLevelName( logging.CRITICAL, '(CRITICAL)' )
    logging.addLevelName( logging.ERROR,    '(EE)' )
    logging.addLevelName( logging.WARNING,  '(WW)' )
    logging.addLevelName( logging.INFO,     '(II)' )
    logging.addLevelName( logging.DEBUG,    '(DD)' )
    logging.addLevelName( logging.NOTSET,   '(NA)' )

    main()

