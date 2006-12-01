#!/usr/bin/python
# -*- coding: utf8 -*-

# Khmer Unicode to Legacy fonts Conversion
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
# This module convertes an *.html file from Unicode to  legacy Khmer format 

import sys
import os
import codecs
from legacyReorder import *
from legacyConverter import *
from FontDataXML import *
import unittest
import StringIO

EURO = unichr(0x20AC)
LF = unichr(13)
CR = unichr(10)
ZWSP = unichr(0x200B)
ZWNJ = unichr(0x200C)
ZWJ = unichr(0x200D)
LEGALCHAR = u" %!@«»,;:(){}*+=-\\/$?" + EURO + LF + CR + ZWNJ + ZWSP + ZWJ
STARTKHMER = u"«»" + ZWNJ + ZWSP + ZWJ
MINUNIC = 0x1780
MAXUNIC = 0x17FF

def convertHTML(inputFile, outputFile, outputFont):
    """converts Khmer Unicode HTML file to Khmer Legacy HTML file
    inputfilename: Khmer Unicode HTML file 
    outputfilename: Khmer Legacy HTML file
    outputFont: font to use for the output in a <font> tag
    """

    if (inputFile == outputFile):
        raise TypeError('input file and output file must be different!')

    fd = FontData()
    if (not fd.isConvertable(outputFont)):        
        raise TypeError('unknown output font ' + outputFont + '!')

    encode = findEncode(inputFile)
    try:
        htmlData = codecs.open(inputFile, encoding = encode)
    except IOError:                
        raise IOError('Cannot open file "' +  inputFile + '" for reading!')

    try:
        fout = codecs.open(outputFile, encoding = encode, mode = "w")
    except IOError:        
        raise IOError('Cannot open file "' +  outputFile + '" for writing!')

    convert(htmlData, fout, outputFont)
    htmlData.close()
    fout.close()

def convert(finobj, foutobj, outputFont):
    '''gets input and output as file-like object, and get fontType
    it analyzes, converts the unicode to legacy and then produce the legacy output.'''

    fd = FontData()
    data = fd.unicodeData(outputFont)
    fontName = fd.defaultFont(outputFont)
    bodyFound = False # <body> not found
    insideTag = True
    insideKhmer = False
    insideComment = False
    validChar = False

    unic = u''
    keep = u''
    for line in finobj:
        i = -1
        if (not bodyFound):                    
            found = line.lower().find('<body')
            if (found == -1):
                found = line.find('<BODY')
            if (found == -1):
                foutobj.write(line)
                continue
            bodyFound = True
            i = found + 4
            keep += line[0 : i + 1] # keep the characters until '<body' 

        while (i < len(line) - 1):
            i += 1
            currChar = line[i]
            val = ord(currChar)

            if (insideComment):
                if (line[i : i+3] == '-->'):
                    insideComment = False
                    keep += '-->'
                    i += 2
                else:
                    keep += currChar
                continue

            if (line[i : i+4] == '<!--') :
                i += 3            
                keep += '<!--'
                insideComment = True
                continue

            if (currChar == '>'):
                insideTag = False
            elif (currChar == '<'):
                insideTag = True

            if (not insideTag and (line[i : i+2] == '&#')):
                entity = ''
                if (line[i+2 : i+3] == 'x'):
                    entity = '0x'
                    j = i + 3
                else:
                    j = i + 2

                while (True):
                    char = line[j : j+1]
                    if (char == ''):
                        break
                    if (char ==  ';'): 
                        j += 1
                        break
                    entity += char;
                    try:
                        val = eval(entity)
                    except SyntaxError:                        
                        entity = entity[ : -1]
                        break
                    j += 1
                val = eval(entity)
                currChar = unichr(val)
                i = j - 1

            if (not insideTag and not insideKhmer and 
                ((val >= MINUNIC) and (val <= MAXUNIC) or (STARTKHMER.find(unichr(val)) != -1))):
                insideKhmer = True
                keep += '<font face="' + fontName + '" size="5">' 
                unic += currChar
                continue
            if (insideKhmer):
                if ((val >= MINUNIC) and (val <= MAXUNIC) or (LEGALCHAR.find(unichr(val)) != -1)):
                    unic += currChar
                    continue
                else:
                    insideKhmer = False
                    unic = reorder(unic)                    
                    legacy = converter(unic, data)
                    keep += legacy.decode('cp1252') + '</font>' + currChar
                    unic = u''
                    continue            
            keep += currChar
        foutobj.write(keep)
        keep = u''

def findEncode(inputFileName):
    '''Receive an inputFileName, find the type of charsert and then return it. 
    If no charset found, it will return utf-8.'''

    #TODO: change this function so that it will use an open file object and use seek() to rewind it
    htmlData = open(inputFileName)
    for line in htmlData:        
        found = line.lower().find("charset=")
        if (found != -1):
            charSet = line[found+8 : ]
            break
        if (line.find("<body") != -1):
            break
    htmlData.close()
    if (found == -1):
        return 'utf-8'
    found = charSet.find('\"')
    if (found != -1):
        charSet = charSet[ : found]
    return charSet

class TestConvertHTML(unittest.TestCase):

    def testSameFile(self):
        # same file raise error
        self.assertRaises(TypeError, convertHTML, 'file1', 'file1', 'abc')

    def testOpenUnavailableFile(self):
        # raise error when file is unavailable
        self.assertRaises(IOError, convertHTML, 'file', 'file1', 'abc')

    def testBodyTag(self):
        # body in second line
        data = u"<html>\n<body></body></html>"
        outputFont = 'abc'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, outputFont)
        self.assertEqual(foutobj.getvalue(),  u"<html>\n<body></body></html>")


    def testKhmer(self):
        # just  កក
        data = u"<html><body>កក</body></html>"
        outputFont = 'abc'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, outputFont)
        self.assertEqual(foutobj.getvalue(),  u"<html><body><font face=\"ABC-TEXT-05\" size=\"5\">kk</font></body></html>")
        # just  ក\nក
        data = u"<html><body>ក\nក</body></html>"
        outputFont = 'abc'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, outputFont)
        self.assertEqual(foutobj.getvalue(),  u"<html><body><font face=\"ABC-TEXT-05\" size=\"5\">k\nk</font></body></html>")
        # all allowed characters in between Khmer
        data = u"<html><body>ក" + u" %!@,;:(){}*+-\\/?" + EURO + u"ក</body></html>"
        outputFont = 'abc'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, outputFont)
        # EURO gets removed!
        self.assertEqual(foutobj.getvalue(),  u'<html><body><font face=\"ABC-TEXT-05\" size=\"5\">k' + ' %!@/;:(){}*=-\\/?k</font></body></html>')

    def testEntity(self):
        # decimal ក
        data = u"<html><body>&#6016;</body></html>"
        outputFont = 'abc'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, outputFont)
        self.assertEqual(foutobj.getvalue(),  u"<html><body><font face=\"ABC-TEXT-05\" size=\"5\">k</font></body></html>")
        # hex ក
        data = u"<html><body>&#x1780;</body></html>"
        outputFont = 'abc'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, outputFont)
        self.assertEqual(foutobj.getvalue(),  u"<html><body><font face=\"ABC-TEXT-05\" size=\"5\">k</font></body></html>")        
        # hex ុ
        data = u"<html><body>&#x1780;</body></html>"
        outputFont = 'abc'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, outputFont)
        self.assertEqual(foutobj.getvalue(),  u"<html><body><font face=\"ABC-TEXT-05\" size=\"5\">k</font></body></html>")        
        # missing ; and symbolic entity
        data = u"<html><body>&1780;&#6016&#6016;&&copy;ក</body></html>"
        outputFont = 'abc'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, outputFont)
        self.assertEqual(foutobj.getvalue(),  u"<html><body>&1780;<font face=\"ABC-TEXT-05\" size=\"5\">kk</font>&&copy;<font face=\"ABC-TEXT-05\" size=\"5\">k</font></body></html>")

    def testComments(self):
        # simple comment
        data = u"<html><body><!--i--></body></html>"
        outputFont = 'abc'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, outputFont)
        self.assertEqual(foutobj.getvalue(),  u"<html><body><!--i--></body></html>")
        # comment in two lines
        data = u"<html><body><!--i\na--></body></html>"
        outputFont = 'abc'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, outputFont)
        self.assertEqual(foutobj.getvalue(),  u"<html><body><!--i\na--></body></html>")
        # comment with unicode inside
        data = u"<html><body><!--កក--></body></html>"
        outputFont = 'abc'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, outputFont)
        self.assertEqual(foutobj.getvalue(),  u"<html><body><!--កក--></body></html>")
        # comment with start comment inside
        data = u"<html><body><!--កក <!-- --></body></html>"
        outputFont = 'abc'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, outputFont)
        self.assertEqual(foutobj.getvalue(),  u"<html><body><!--កក <!-- --></body></html>")

if __name__ == '__main__':
    unittest.main()
