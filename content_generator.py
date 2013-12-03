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
import subprocess

def remove_suffix(in_string, suffix):
    if in_string.endswith(suffix):
        return in_string[:-len(suffix)]
    return in_string

def list_directory(root, path, suffix):

    logging.debug("list_directory(root='%s', path='%s', suffix='%s')",
        root, path, suffix)

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
        link_path = os.path.join('/', path, dir_name)
        logging.debug("  add dir '%s'+'%s'='%s'", path, dir_name, os.path.join('/', path, dir_name))
        print("<a href = %s>%s</a><br>" % (link_path, dir_name) )
    print("</p>")


    print("<p>")
    for file_name in files:
        link_path = os.path.join('/', path, file_name)
        logging.debug("  add file '%s'+'%s'='%s'", path, file_name, link_path)
        print("<a href = %s>%s</a><br>" % (link_path, file_name) )
    print("</p>")

    print("</body></html>")

def display_file(root, path, asciidoc_processor, suffix):

    logging.debug("display_file(root='%s', path='%s', suffix='%s')",
        root, path, suffix)

    _in_file = os.path.join(root, path)
    
    _out_file = path[:-len(suffix)] + ".html"

    logging.debug("  read from file '%s'", _in_file )
    logging.debug("  write to file '%s'", _out_file )

    _asciidoc_output = subprocess.Popen(
        [asciidoc_processor, '-a', 'max-width=1024px', '--out-file', '-', _in_file],
        stdout=subprocess.PIPE).communicate()[0]

#    _asciidoc_retval = os.system("%s -a max-width=1024px --out-file - %s" % 
#                                 (asciidoc_processor, _in_file))
    
    #print open(_out_file).read()
    print _asciidoc_output


def generate_html(root, path, asciidoc_processor='asciidoc', suffix='.asciidoc.txt'):
    """does the actual work. is getting called by main() or directly by
       a http server or a test
    """
    try:
        prepared_path = remove_suffix(path, 'index.html').strip('/')

        full_local_dir = os.path.join(root, prepared_path)

        if os.path.isdir(full_local_dir):
            list_directory(root, prepared_path, suffix)
        elif os.path.isfile(full_local_dir):
            display_file(root, prepared_path, asciidoc_processor, suffix)
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

            logging.error("root='%s' path='%s', prepared_path='%s' full='%s'",
                root, path, prepared_path, full_local_dir)
            return -1

    except Exception, ex:
        print ex
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
