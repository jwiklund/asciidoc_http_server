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

"""generates a html content as response to a root folder and a sub url
   depending on the sub url an asciidoc page or a content page will be
   generated
"""
    
import optparse
import sys
import os
import logging

def generate_html(root, path, suffix='.asciidoc.txt'):        
    """does the actual work. is getting called by main() or directly by
       a http server or a test
    """
    
    files = [filen for filen in os.listdir(root)
             if os.path.isfile(os.path.join(root, filen))
             and filen.endswith(suffix)]
    
    
    if path == "/" or path == "/index.html":
        print("<html>"
              "<head><title>scitics public knowledge base</title></head>"
              "<body>")
        
        print("<p>"
              "you accessed path: '%s'<br>"
              "root is:           '%s'"
              "</p>" % ( path, root))
        
        for filen in files:
            print("<p><a href = %s>%s</a></p>" % (filen, filen) )
        print("</body></html>")
            
    elif path[1:] in files:
        _in_file = os.path.join(root, path[1:])
        _out_file = "~" + path[1:-len(suffix)] + ".html"
        logging.info("<p>%s</p>", _in_file )
        
        _asciidoc_retval = os.system("asciidoc --out-file %s %s" % 
                                     (_out_file, _in_file))
        
        print open(_out_file).read()
        
        logging.info("<p>transform to %s</p>", _out_file )
        
    else:
        print("<html>"
              "<head><title>scitics public knowledge base</title></head>"
              "<body>")
        
        print("<p>"
              "UNKNOWN<br>"
              "you accessed path: '%s'<br>"
              "root is:           '%s'"
              "</p>" % ( path, root))

        print("</body></html>")
    
        return -1
    
    return 0
    
def main():
    """decouples the main function from global space. parses command line
       and calls generate_html()
    """

    parser = optparse.OptionParser()

    parser.add_option("-r", "--root", dest = "root",
                      help = "asciidoc document folder", metavar = "path")
    parser.add_option("-f", "--filename", dest = "filename",
                      help = "file name", metavar = "file")

    (options, _) = parser.parse_args()

    sys.exit(generate_html(options.root, options.filename))

if __name__ == "__main__":
    main()
