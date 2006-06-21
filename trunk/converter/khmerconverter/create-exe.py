#!/usr/bin/python
# -*- coding: utf8 -*-

# Khmer Legacy to Khmer Unicode Conversion and Vice Versa
# (c) 2006 Open Forum of Cambodia, all rights reserved.
#
# Version 1.0
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

from distutils.core import setup
import py2exe
import sys
sys.argv.append("py2exe")

setup(console = [{"script": 'khmerConverter.py'}],
packages = ['modules'])
