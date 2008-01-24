#!/usr/bin/python
# -*- coding: utf8 -*-

# Khmer Unicode to Khmer Legacy fonts Conversion
# Copyright(c) 2006-2008 Khmer Software Initiative
#               www.khmeros.info
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
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

from FontDataXML import FontData
import legacyReorder
import legacyConverter
import unittest
import tempfile
import os


def convertTxtFile(inputFile, outputFile, outputFont):
    """
    This function creates plain text file from the khmer unicode to legacy.
    """

    if (inputFile == outputFile):
        raise TypeError('Input file and output file must be different!')

    fd = FontData()
    if (not fd.isConvertable(outputFont)):
        raise TypeError('Unknown output font ' + outputFont + ' !')

    try:
        fileIn = open(inputFile, 'r')
    except IOError:
        raise IOError('Cannot open file "' +  inputFile + '" for reading!')

    try:
        fileOut = open(outputFile, 'w')
    except IOError:
        raise IOError('Cannot open file "' +  outputFile + '" for writing!')

    data = fd.unicodeData(outputFont)

    # reading line by line from the input file, until end of file.
    for line in fileIn:
        result = line.decode('utf-8')
        result = legacyReorder.reorder(result)
        result = legacyConverter.converter(result, data)
        fileOut.write(result)

    fileIn.close()
    fileOut.close()


class TestConvertTxt(unittest.TestCase):

    def testSameFile(self):
        # same file raise error
        self.assertRaises(TypeError, convertTxtFile, 'file1', 'file1', 'fontname')

    def testNotFound(self):
        # raise error when file is unreadable
        self.assertRaises(TypeError, convertTxtFile, 'file', 'file1', 'fontname')

    def testConversion(self):
        handle, filename = tempfile.mkstemp()
        tmpFile = open(filename, 'w')
        tmpFile.write(u'កខគ'.encode('utf-8'))
        tmpFile.close()
        # create a usable filename for output
        tmpFile = tempfile.TemporaryFile()
        outputFilename = tmpFile.name
        tmpFile.close()

        convertTxtFile(filename, outputFilename, 'abc')
        tmpFile = open(outputFilename, 'r')
        result = tmpFile.readline()
        tmpFile.close()

        os.remove(filename)
        os.remove(outputFilename)

        self.assertEqual(result.decode('utf-8'), 'kxK')

if __name__ == '__main__':
    unittest.main()
