#!/usr/bin/python
# -*- coding: utf8 -*-

# Khmer Unicode to Khmer Legacy fonts Conversion
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
#       Jens Herden (jens@khmeros.info)

import unittest
from FontDataXML import FontData


# testing the content of fontdata.xml

class TestFontData(unittest.TestCase):

    dataClass = FontData()

    def setUp(self):
        self.dataClass.readXML("fontdata.xml")

    def testABCDataLegacy(self):
        data = self.dataClass.legacyData("abc")
        self.assertEqual(data[1][0xb2], unichr(0x201c))
        self.assertEqual(data[1][0xb3], unichr(0x201d))

    def testABCDataUnicode(self):
        data = self.dataClass.unicodeData("abc")
        self.assertEqual(data[0][0][unichr(0x201c)], chr(0xb2))
        self.assertEqual(data[0][0][unichr(0x201d)], chr(0xb3))
        self.assertEqual(data[0][0][u'«'], chr(0xb2))
        self.assertEqual(data[0][0][u'»'], chr(0xb3))

    def testLimonDataLegacy(self):
        data = self.dataClass.legacyData("limon")
        self.assertEqual(data[1][0x7b], unichr(0x201c))
        self.assertEqual(data[1][0x7d], unichr(0x201d))

    def testLimonDataUnicode(self):
        data = self.dataClass.unicodeData("limon")
        self.assertEqual(data[0][0][unichr(0x201c)], chr(0x7b))
        self.assertEqual(data[0][0][unichr(0x201d)], chr(0x7d))
        self.assertEqual(data[0][0][u'«'], chr(0x7b))
        self.assertEqual(data[0][0][u'»'], chr(0x7d))
        self.assertEqual(data[0][0][u'ឲ'], chr(0xbb))

##    def testDumpLimon(self):
##        data = self.dataClass.unicodeData("limon")
##        print "data: ", data[1]
##        print "data0: ", data[0][0]
##        print "data1: ", data[0][1]
##        print "data2: ", data[0][2]

if __name__ == '__main__':
    unittest.main()
