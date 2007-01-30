#!/usr/bin/python
# -*- coding: utf8 -*-

# Khmer Legacy fonts to Khmer Unicode Conversion
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
# This module creates a Text file in Khmer unicode format from legacy
# input file.

import unicodeProcess
import unicodeReorder
from FontDataXML import FontData
import unittest

def convertTxtFile(inputFileName, outputFileName, fontType, encoding):
    """
    converts Khmer legacy plain text file and produce a unicode output file
    inputfilename: Legacy plain text file
    outputfilename: Khmer Unicode plain text file
    fontType: type "abc" or font name "ABC-TEXT-5"
    encoding: cp1252, utf-8, iso-8859-1
    """
    if (inputFileName == outputFileName):
        raise TypeError('input file and output file must not be the same!')

    fd = FontData()
    if (not fd.canDecode(encoding)):
        raise TypeError('unknow encoding!')
    
    try:
        fin = open(inputFileName, "r")
    except IOError:        
        raise IOError('Cannot open file "' +  inputFileName + '" for reading!')
    
    try:
        fout = open(outputFileName, "w")
    except IOError:        
        raise IOError('Cannot open file "' +  outputFileName + '" for writing!')
    
    data = fd.legacyData(fontType)
    # reading line by line from the input file, until end of file.
    for line in fin:
        sin = fd.changeEncoding(line, encoding)
        result = unicodeProcess.process(sin, data)
        bufout = unicodeReorder.reorder(result)
        fout.write(bufout.encode('utf-8'))

    fin.close()
    fout.close()


class TestConvertTxt(unittest.TestCase):

    def setUp(self):
        pass
    
    def testSameFile(self):
        # same file raise error
        self.assertRaises(TypeError, convertTxtFile, 'file1', 'file1', None, None)

    def testEncoding(self):
        # assert error if file is unreadable
        self.assertRaises(TypeError, convertTxtFile, 'file', 'file1', None, 'blablabla')

    def testConversion(self):
        import tempfile
        import os
        handle, filename = tempfile.mkstemp()
        tmpFile = open(filename, 'w')
        tmpFile.write('kxK')
        tmpFile.close()
        # create a usable filename for output
        #TODO: this does not work here, Jens
        tmpFile = tempfile.TemporaryFile()
        outputFilename = tmpFile.name
        tmpFile.close()
        
        convertTxtFile(filename, outputFilename, 'abc', 'cp1252')
        tmpFile = open(outputFilename, 'r')
        result = tmpFile.readline()
        tmpFile.close()
        
        os.remove(filename)
        os.remove(outputFilename)
        
        self.assertEqual(result.decode('utf-8'), u'កខគ')
        
if __name__ == '__main__':
    unittest.main()
