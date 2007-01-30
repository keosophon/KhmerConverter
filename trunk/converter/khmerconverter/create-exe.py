#!/usr/bin/python
# -*- coding: utf8 -*-

# Khmer Legacy to Khmer Unicode Conversion and Vice Versa
# (c) 2006 The WordForge Foundation, all rights reserved.
#
# Version 1.3 (30 January 2007)
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public License
# as published by the Free Software Foundation; either version 2.1
# of the License, or (at your option) any later version.
#
# See the LICENSE file for more details.
#
# Developed by:
#       Hok Kakada (hokkakada@khmeros.info)
#       Keo Sophon (keosophon@khmeros.info)
#       San Titvirak (titvirak@khmeros.info)
#       Seth Chanratha (sethchanratha@khmeros.info)
#
# This program creates a Plain Text, OpenOffice.org Writer (odt), or HTML file
# in Khmer Unicode/Legacy format from Legacy/Unicode input file respectively.
#
# create an executable file on Windows
# command: python setup.py
# Requirements: distutils package and py2exe installer

import glob
import os
import sys
from distutils.core import setup
import py2exe

def files(folder):
    for path in glob.glob(folder+'/*'):
        if os.path.isfile(path):
            yield path

data_files=[
            ('.', glob.glob(sys.prefix+'/DLLs/tix81*.dll')),
            ('tcl/tix8.1', files(sys.prefix+'/tcl/tix8.1')),
            ('tcl/tix8.1/bitmaps', files(sys.prefix+'/tcl/tix8.1/bitmaps')),
            ('tcl/tix8.1/pref', files(sys.prefix+'/tcl/tix8.1/pref')),
           ]

setup(
      script_args=['py2exe'],
      data_files=data_files,
      windows=[{"script": "khmerconverter.py", "icon_resources": [(1, "converter.ico")]}],
      packages = ['modules']
     )
