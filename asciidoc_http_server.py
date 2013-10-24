#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# file: asciidoc_http_server.py
#
# Copyright 2011 - 2013 scitics GmbH
#
# Information  contained  herein  is  subject  to change  without  notice.
# scitics GmbH  retains ownership and  all other rights  in this software.
# Any reproduction of the software or components thereof without the prior
# written permission of scitics GmbH is prohibited.

"""docstring"""

import optparse
import BaseHTTPServer
import SocketServer
import logging
import sys
import socket
import os
import subprocess

class ServerHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    """docstring"""

    def __init__(self, eins, zwei, drei):
        BaseHTTPServer.BaseHTTPRequestHandler.__init__(self, eins, zwei, drei)

        # should avoid socket.error "address already in use" but has no effect
        self.server.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    def do_HEAD(self):
        """docstring"""
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
    
    def do_GET(self):
        """docstring"""
        
        _command  = [sys.executable]
        _command += [os.path.join(
            os.path.dirname(__file__), 
            "content_generator.py") ]
        _command += ['-r', self.server.root]
        _command += ['-f', self.path]
        
        _process = subprocess.Popen(args=_command, stdout=subprocess.PIPE)
        _stdout, _stderr = _process.communicate()
        _return = _process.returncode
        
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
    """docstring"""
    
    parser = optparse.OptionParser()

    parser.add_option("-r", "--root", dest = "root", default = ".",
                      help = "asciidoc document folder", metavar = "path")

    parser.add_option("-p", "--port", dest = "port", default = 8000,
                      help = "port used for http", metavar = "port-nr")

    (options, _) = parser.parse_args()

    if hasattr(socket, 'setdefaulttimeout'):
        socket.setdefaulttimeout(2)

    httpd = SocketServer.TCPServer(("", int(options.port)), ServerHandler)
    
    # bad: refactor
    httpd.root = options.root

    print "serving at port", options.port
    print "serving folder ", os.path.abspath(options.root)

    httpd.serve_forever()

if __name__ == "__main__":
    main()
    
