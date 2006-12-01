#!/usr/bin/python
# -*- coding: utf8 -*-

# Khmer Legacy fonts to Khmer Unicode Conversion
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
# This module creates an HTML  file in Khmer unicode format from legacy
# input file.

import sys
import codecs
from unicodeReorder import *
from unicodeProcess import *
from FontDataXML import *
import htmlentitydefs
import unittest
import StringIO

LF = unichr(13)
CR = unichr(10)
MAXLEGACY = 0xFF

def convertHTMLFile(inputFile, outputFile, fontType):
    """converts Khmer Legacy HTML file to Khmer Unicode HTML file
    inputfilename: name of Khmer Legacy HTML file you wanna convert.
    outputfilename: Khmer Unicode HTML file)
    fontType: font for the conversion 
    """

    if (inputFile == outputFile):
        raise TypeError('input file and output file must not be the same!')

    fd = FontData()

    if (not fd.isConvertable(fontType)):        
        raise TypeError('unknown output font ' + fontType + '!')

    encode = findEncode(inputFile)

    try:        
##        htmlData = codecs.open(inputFile, encoding = encode)
        #TODO: open file with encoding
            htmlData = open(inputFile)
    except IOError:        
        raise IOError('Cannot open file "' +  inputFile + '" for reading!')
    try:
        fout = codecs.open(outputFile, encoding = "utf-8", mode = "w")
    except IOError:        
        raise IOError('Cannot open file "' + outputFile +  '" for writing!')

    convert(htmlData, fout, fontType, encode)
    htmlData.close()
    fout.close()

def convert(finobj, foutobj, fontName, encode):
    '''conversion process.
    finobj : input file-like object in legacy format.
    foutobj : output file-like object in unicode format after conversion
    fontName : legacy font name of the input file.
    encode : the encoding that input file use.'''    

    fd = FontData()
    fontType = fd.typeForFontname(fontName)
    data = fd.legacyData(fontType)     
    bodyFound = False # <body> not found
    insideTag = True
    insideLegacy = False
    insideComment = False
    legacy = ''
    keep = u''
    setCharSet = '\n<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />\n'
    headPart = ''
    for line in finobj:
        i = -1
        if (not bodyFound):
            found = line.lower().find('<body')
            if (found == -1):
                headPart += line
                continue

            bodyFound = True
            i = found - 1
            headPart += line[ : found]
            # modify head
            headPartLower = headPart.lower()
            foundHead = headPartLower.find('<head')
            if (foundHead == -1):
                foutobj.write(headPart + '\n<head>' + setCharSet + '</head>\n')
            else:
                foundCharset = headPartLower.find('charset=', foundHead + 5)
                if (foundCharset == -1):
                    headEnd = headPartLower.find('>', foundHead + 5)
                    if (headEnd == -1):
                        # very broken HTML
                        foutobj.write(headPart + setCharSet)
                    else:
                        foutobj.write(headPart[ : headEnd + 1] + setCharSet + headPart[headEnd + 1: ])
                else:
                    # charset found!
                    foutobj.write(headPart[ : foundCharset+8] + 'utf-8' + headPart[foundCharset+8+len(encode) : ])


        while (i < len(line) - 1):
            i += 1
            val = ord(line[i])
            currChar = unichr(val)

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
                # work around for wrong HTML
                if (fontType in ['abc', 'abc-zwsp', 'limon']):
                    if (val == 8216):
                        val = 0x91
                    elif (val == 8217):
                        val = 0x92
                        
                currChar = unichr(val)
                i = j - 1
                
            # try convert an entity such as &copy; to the unicode character
            if (currChar == '&'):
                found = line[i : ].find(";")
                if (found != -1):
                    entity= line[i+1 : i+found]
                    if (htmlentitydefs.entitydefs.has_key(entity)):
                        try:
                            val = ord(htmlentitydefs.entitydefs[entity])
                        except TypeError:
                            val = eval(htmlentitydefs.entitydefs[entity][2 : len(htmlentitydefs.entitydefs[entity]) - 1])                        
                        currChar = unichr(val)
                        i += found

            if ((not insideTag) and (not insideLegacy) and (currChar != u'>') and (currChar != CR) and (currChar != LF) and (val <= MAXLEGACY)):
                insideLegacy = True
                legacy += chr(val)
                continue

            if ( insideLegacy):
                if ((not insideTag) and (currChar != CR) and (currChar != LF) and (val <= MAXLEGACY)):
                    legacy += chr(val)
                    continue
                else:
                    insideLegacy = False
                    unic = process(legacy, data)
                    unic = reorder(unic)
                    keep += unic + currChar
                    legacy = ''
                    continue
            keep += currChar
        foutobj.write(keep)
        keep = u''

def findEncode(inputFileName):
    '''Receive an inputFileName, find the type of charset and then return it. 
    If no charset found, it will return utf-8.'''
    
    htmlData = open(inputFileName)
    for line in htmlData:
        found = line.find("charset=")
        if (found != -1):
            charSet = line[found+8 : ]
            break
    htmlData.close()
    if (found == -1):
       return 'utf-8'

    found = charSet.find('\"')
    if (found != -1):
        charSet = charSet[ : found]
    return charSet

class TestConvertHTMLFile(unittest.TestCase):

    META = '<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />'
    METALF = '\n' + META + '\n'

    def testSameFile(self):
        # same file raise error
        self.assertRaises(TypeError, convertHTMLFile, 'file1', 'file1', 'abc')

    def testOpenUnavailableFile(self):
        # raise error when file is unavailable
        self.assertRaises(IOError, convertHTMLFile, 'file', 'file1', 'abc')

    def testMetaCharSet(self):
        # MetaCharSet After <TITLE></TITLE>
        data ='<html><head><TITLE>sala</TITLE><meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1" /></head><body></body></html>'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, 'abc', 'iso-8859-1')
        self.assertEqual(foutobj.getvalue(), u'<html><head><TITLE>sala</TITLE>' + self.META + '</head><body></body></html>')

        # No MetaCharSet <TITLE></TITLE>
        data ='<html><head><TITLE>sala</TITLE></head><body></body></html>'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, 'abc', 'iso-8859-1')
        self.assertEqual(foutobj.getvalue(), u'<html><head>' + self.METALF + '<TITLE>sala</TITLE></head><body></body></html>')    
        # No <head>
        data ='<html><body></body></html>'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, 'abc', 'iso-8859-1')
        self.assertEqual(foutobj.getvalue(), u'<html>\n<head>' + self.METALF + '</head>\n<body></body></html>')    

    def testComments(self):                
        data ='<html><head><TITLE>sala</TITLE></head><body><!--include virtual="/modules/cat_pages/Tourism/tourismTop3.asp" --></body></html>'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, 'abc','iso-8859-1')
        self.assertEqual(foutobj.getvalue(), u'<html><head>' + self.METALF + '<TITLE>sala</TITLE></head><body><!--include virtual="/modules/cat_pages/Tourism/tourismTop3.asp" --></body></html>')

    def testConversion(self):
        # convert one character
        data ='<html><head><TITLE>sala</TITLE></head><body>k</body></html>'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, 'abc', 'iso-8859-1')
        self.assertEqual(foutobj.getvalue(), u'<html><head>' + self.METALF + u'<TITLE>sala</TITLE></head><body>ក</body></html>')

        # convert two character
        data ='<html><head><TITLE>sala</TITLE></head><body>kx</body></html>'
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, 'abc', 'iso-8859-1')
        self.assertEqual(foutobj.getvalue(), u'<html><head>' + self.METALF + u'<TITLE>sala</TITLE></head><body>កខ</body></html>')       

    def testEntity(self):
        # test character with value less than 0xFF
        data ='<html><head><TITLE>sala</TITLE></head><body>&#x6b;</body></html>'        
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, 'abc', 'iso-8859-1')
        self.assertEqual(foutobj.getvalue(), u'<html><head>' + self.METALF + u'<TITLE>sala</TITLE></head><body>ក</body></html>')        

        # test &#x1780;
        data ='<html><head><TITLE>sala</TITLE></head><body>&#x1780;</body></html>'        
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, 'abc', 'iso-8859-1')
        self.assertEqual(foutobj.getvalue(), u'<html><head>' + self.METALF + u'<TITLE>sala</TITLE></head><body>ក</body></html>')

       # test &#6016;
        data ='<html><head><TITLE>sala</TITLE></head><body>&#6016;</body></html>'        
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, 'abc', 'iso-8859-1')
        self.assertEqual(foutobj.getvalue(), u'<html><head>' + self.METALF + u'<TITLE>sala</TITLE></head><body>ក</body></html>')

        # test entities with no ;
        data ='<html><head><TITLE>sala</TITLE></head><body>&#6016&#x1780</body></html>'        
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj, foutobj, 'abc', 'iso-8859-1')
        self.assertEqual(foutobj.getvalue(), u'<html><head>' + self.METALF + u'<TITLE>sala</TITLE></head><body>កក</body></html>')

        # test &copy;
        data ='<html><head><TITLE>sala</TITLE></head><body>&copy;</body></html>'        
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj,foutobj,'abc','iso-8859-1')
        self.assertEqual(foutobj.getvalue(), u'<html><head>' + self.METALF + u'<TITLE>sala</TITLE></head><body>្ច</body></html>')    

        # test &copy
        data ='<html><head><TITLE>sala</TITLE></head><body>&copy</body></html>'        
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj,foutobj,'abc','iso-8859-1')
        self.assertEqual(foutobj.getvalue(), u'<html><head>' + self.METALF + u'<TITLE>sala</TITLE></head><body>ចៀ័ផយ</body></html>')
        # test &amp;
        data ='<html><head><TITLE>sala</TITLE></head><body>&amp;</body></html>'        
        finobj = StringIO.StringIO(data)
        foutobj = StringIO.StringIO()
        convert(finobj,foutobj,'abc','iso-8859-1')
        self.assertEqual(foutobj.getvalue(), u'<html><head>' + self.METALF + '<TITLE>sala</TITLE></head><body>' + unichr(0x17d0) + '</body></html>')

if __name__ == '__main__':
    unittest.main()
