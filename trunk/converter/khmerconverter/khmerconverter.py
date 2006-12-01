#!/usr/bin/python
# -*- coding: utf8 -*-

# Khmer Legacy to Khmer Unicode Conversion and Vice Versa
# (c) 2006 Open Forum of Cambodia, all rights reserved.
#
# Version 1.1 (01 December 2006)
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

from optparse import OptionParser
from modules import FontDataXML
import sys
import os

if (sys.argv[0].endswith('py')):
    py = 'python '
else:
    py = ''
usage = py + """%prog [OPTION] input [output]
   or: """ + py + """%prog [OPTION]\n
Font encoding converter for Khmer text.
Converts between legacy and Unicode in both directions.
Currently supported file formats are: 
    Plain Text
    OpenOffice writer document
    HTML"""

strVersion = """%prog Version 1.0\n
Copyright (C) 2006 Open Forum of Cambodia. www.khmeros.info.
This is free software. You may redistribute copies of it under the terms of
the GNU Lesser General Public License <http://www.gnu.org/licenses/lgpl.html>.
There is NO WARRANTY, to the extent permitted by law.
Written by Hok Kakada, Keo Sophon, San Titvirak, Seth Chanratha.
"""
parser = OptionParser(usage = usage, version = strVersion)

parser.add_option("-l", "--list", action="store_true", dest="listFont", default=False, 
                  help="list all supported fonts")

parser.add_option("-c", "--codec", action="store_true", dest="listcodectypes", default=False, 
                  help="list all supported codecs for text files")

parser.add_option("-o", "--oldfont", action="store_true", dest="oldfont", default=False,
                  help="convert from unicode to old fonts (legacy)")

parser.add_option("-e", "--encoding", dest="encoding", action="store", type="string",
                  help="codec for the input file, default is 'cp1252'", metavar="codec", default="cp1252")

parser.add_option("-f", "--font", dest="font", action="store", type="string",
                  help="fontname for output encoding, default is 'abc-zwsp'", metavar="fontname", default="abc-zwsp")

parser.add_option("-s", "--size", dest="fontSize", action="store", type="int",
                  help="force the program to use specific size for khmer font", metavar="value", default=None)

parser.add_option("-t", "--timer", action="store_true", dest="showtimer", default=False, 
                  help="print the needed time for the conversion")

(options, args) = parser.parse_args()
argc = len(args)

fd = FontDataXML.FontData()

# print all codec type
if (options.listcodectypes):
    print 'Supported input encodings:', fd.listEncodingTypes()
    sys.exit()

# print all font names
if (options.listFont):
    print 'Supported fonts:'
    l = fd.listFontNames()
    for line in l:
        print line
    sys.exit()

if (len(sys.argv) == 1):
    from modules import converterGUI
    sys.exit()

if (argc == 0):
    sys.stderr.write("Please enter a file name or a legal option!\nUse the --help option for more info.\n")
    sys.exit()

inputFileName = args[0]
if not os.path.exists(args[0]):
    sys.stderr.write(inputFileName + ' does not exist!\n')
    sys.exit()

if (argc < 2):
    #output file is in the same folder as input file
    (path, filename) = os.path.split(inputFileName)
    outputFileName = os.path.join(path, 'converted-' + filename)
else:
    outputFileName = args[1] # User give outputFileName by her own
    if (inputFileName == outputFileName):
        sys.stderr.write("Input file and output file must be different!\n")
        sys.exit()

    (path, filename) = os.path.split(outputFileName)

    # check if output folder entered by user exist
    if (path and not os.path.exists(path)):
        sys.stderr.write('The path does not exist!\n')
        sys.exit()

# check if output file already exist
if (os.path.exists(outputFileName)):
    sys.stderr.write('The output file is already existed!\n')
    sys.exit()

if (options.showtimer):
    timer = time.clock()

# convert from unicode to legacy
if (options.oldfont):
    if (inputFileName.endswith('.odt')):
        from modules import legacyConvertOdt
        converter = legacyConvertOdt.legacyConvertOdt()
        converter.convertOdtFile(inputFileName, outputFileName, options.font, options.fontSize)
    elif(inputFileName.endswith('.htm') or inputFileName.endswith('.html')):
        from modules import legacyConvertHTML
        legacyConvertHTML.convertHTML(inputFileName, outputFileName, options.font)
    else:
        from modules import legacyConvertText
        legacyConvertText.convertTxtFile(inputFileName, outputFileName, options.font)
# convert from legacy to unicode
else:
    if (inputFileName.endswith('.odt')):
        from modules import unicodeConvertOdt
        converter = unicodeConvertOdt.unicodeConvertOdt()
        converter.convertOdtFile(inputFileName, outputFileName, options.font, options.fontSize)
    elif(inputFileName.endswith('.htm') or inputFileName.endswith('.html')):
        from modules import unicodeConvertHTML
        unicodeConvertHTML.convertHTMLFile(inputFileName, outputFileName, options.font)
    else:
        from modules import unicodeConvertText
        unicodeConvertText.convertTxtFile(inputFileName, outputFileName, options.font, options.encoding)

if (options.showtimer):
    timer = time.clock()
    print ">>> Total conversion time:", timer, 'seconds'
