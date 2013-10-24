#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# file: test_content_generator.py
#
# Copyright 2011 - 2013 scitics GmbH
#
# Information  contained  herein  is  subject  to change  without  notice.
# scitics GmbH  retains ownership and  all other rights  in this software.
# Any reproduction of the software or components thereof without the prior
# written permission of scitics GmbH is prohibited.

import sys
import os
import subprocess

def main():

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
    
