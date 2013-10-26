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

""" just implements some sort of smoke test for content_generator. 
    no real testing yet.
"""
import sys
import os
import subprocess

def main():
    """currently just run content_generator in a non-intrusive way"""

    _command  = [sys.executable]
    _command += [os.path.join(
        os.path.dirname(__file__), 
        "content_generator.py") ]
    _command += ['-r', '.']
    _command += ['-f', 'index.html']

    print _command
    
    _process = subprocess.Popen(args=_command, stdout = subprocess.PIPE)
    _stdout, _stderr = _process.communicate()
    _return = _process.returncode
    
    print _stdout
    print _stderr
    print _return

if __name__ == "__main__":
    main()
    
