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

def list_directory(root, path, suffix):

    local_path = os.path.join(root, path)

    files = sorted([filen for filen in os.listdir(local_path)
             if os.path.isfile(os.path.join(local_path, filen))
             and filen.endswith(suffix)])

    directories = sorted([filen for filen in os.listdir(local_path)
             if os.path.isdir(os.path.join(local_path, filen))
             and filen != ".git"])

    print("<html>"
          "<head><title>scitics public knowledge base</title></head>"
          "<body>")

    print("<p>"
          "you accessed path: '%s'<br>"
          "</p>" % [path])


    print("<p>")
    for dir_name in directories:
        print("<a href = %s>%s</a><br>" % (dir_name, dir_name) )
    print("</p>")


    print("<p>")
    for file_name in files:
        print("<a href = %s>%s</a><br>" % (file_name, file_name) )
    print("</p>")

    print("</body></html>")


def generate_html(root, path, asciidoc_processor='asciidoc', suffix='.asciidoc.txt'):
    """does the actual work. is getting called by main() or directly by
       a http server or a test
    """
    try:
        prepared_path = path.lstrip('/').rstrip('index.html')

        full_local_dir = os.path.join(root, prepared_path)

        if os.path.isdir(full_local_dir):
            list_directory(root, prepared_path, suffix)
        elif os.path.isfile(full_local_dir):
            print "'%s' is a file" % full_local_dir
        else:
            print "ERROR root='%s' path='%s' full='%s'" %(root, path.rstrip('index.html'),full_local_dir)
    except Exception, ex:
        print ex


    return

    files = sorted([filen for filen in os.listdir(root)
             if os.path.isfile(os.path.join(root, filen))
             and filen.endswith(suffix)])

    directories = sorted([filen for filen in os.listdir(root)
             if os.path.isdir(os.path.join(root, filen))
             and filen != ".git"])

    if path == "/" or path == "/index.html":
        print("<html>"
              "<head><title>scitics public knowledge base</title></head>"
              "<body>")

        print("<p>"
              "you accessed path: '%s'<br>"
              "root is:           '%s'"
              "</p>" % ( path, root))

        print("<p>")
        for dir_name in directories:
            print("<a href = %s>%s</a><br>" % (dir_name, dir_name) )
        print("</p>")


        print("<p>")
        for file_name in files:
            print("<a href = %s>%s</a><br>" % (file_name, file_name) )
        print("</p>")

        print("</body></html>")

    elif path[1:] in files:
        _in_file = os.path.join(root, path[1:])
        _out_file = "~" + path[1:-len(suffix)] + ".html"
        logging.info("<p>%s</p>", _in_file )

        _asciidoc_retval = os.system("%s -a max-width=1024px --out-file %s %s" % 
                                     (asciidoc_processor, _out_file, _in_file))
        
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
    parser.add_option("-a", "--asciidoc-path", dest = "asciidoc_path",
                      default = "asciidoc", help = "path to asciidoc",
                      metavar = "path")

    (options, _) = parser.parse_args()

    sys.exit(generate_html(options.root, options.filename, options.asciidoc_path))

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
