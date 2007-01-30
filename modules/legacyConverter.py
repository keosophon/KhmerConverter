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
#       Hok Kakada (hokkakada@khmeros.info)
#       Keo Sophon (keosophon@khmeros.info)
#       San Titvirak (titvirak@khmeros.info)
#       Seth Chanratha (sethchanratha@khmeros.info)
#
# This program converts an reordered unicode string based on legacy style to legacy font

import unittest
import sys

#convert from unicode to legacy
def converter(sin, data):
    '''sin as reordered unicode string based on legacy style
        data the font data for the conversion
    returns legacy string where unkown unicode codepoints are dropped
    '''
    dicts = data[0] # dictionary not in unicode range
    replaceData = data[1] # list with character replacement values
    sout = ''
    listLength = len(replaceData)
    i = 0
    end = len(sin)
    while (i < end):
        for j in range( len(dicts)-1, -1, -1):
            if (dicts[j] == None):
                continue
            try:
                sout += dicts[j][sin[i : i+j+1]]
                i += j +1
                break
            except KeyError:
                continue

        else:
            c = sin[i]
            n = ord(c) - 0x1780
            if ((n >= 0) and (n < listLength)):
                sout += replaceData[n]
            elif (ord(c) < 0x7f ): # keep ascii characters
                sout += c.encode('cp1252')
            i += 1
    return sout

class TestConvert(unittest.TestCase):
    
    MARK = unichr(0x17EA)
    condenseData1 = {
        unichr(0x200b):chr(0x20), #ZWSP
        unichr(0x200c):"",  #ZWNJ
        unichr(0x200d):"" # ZWJ
        }
    condenseData2 = {u'បា': 'BAA', u'្ក':'Cok', u'្ស':'Cos', MARK + u'ី':'I'}
    condenseData3 = {
        MARK + MARK +u'៉':chr(0xFA), # Musekatoan (U long)
        MARK + MARK +u'៊':chr(0xFA), # Trisap (U long)
        }
    condenseData6 = {
        u'ខ្ញ'+ MARK + u'ុំ':chr(0xB4) # ខ្ញុំ one code point in  limon
        }
    replaceData = ['k', 'x', 'K', 'X']
    #dicts = [condenseData1, condenseData2, condenseData3]
    dicts = [condenseData1, condenseData2, condenseData3, None, None, condenseData6]
    data = [dicts, replaceData]


    def setUp(self):
        pass
 
    def testConversion(self):
        self.assertEqual(converter(unichr(0x200b), self.data), chr(0x20)) # in dict1
        self.assertEqual(converter(unichr(0x200c), self.data), "")
        self.assertEqual(converter(u'បា', self.data), 'BAA') # in dict2
        self.assertEqual(converter(u'្ក', self.data), 'Cok') 
        self.assertEqual(converter(u'្ស'+ self.MARK + self.MARK + u'៊' + self.MARK + u'ី', self.data), 'Cos' +  chr(0xFA) + 'I')  # in dict3
        self.assertEqual(converter(u'ខ្ញ'+ self.MARK + u'ុំ',self.data), chr(0xB4)) # in dict6
        self.assertEqual(converter(u'ក', self.data), 'k') # in list
        self.assertEqual(converter(u'ខ', self.data), 'x')
        self.assertEqual(converter(u'ឃ', self.data), 'X')

    def testNoConversion(self):
        # keep characters we do not know
        self.assertEqual(converter(u'?', self.data), '?') # neither in dict nor in list
        self.assertEqual(converter(u'\n', self.data), '\n')
        self.assertEqual(converter(u'', self.data), '')
        # remove unknown unicode character
        self.assertEqual(converter(unichr(255), self.data), '')
        self.assertEqual(converter(unichr(0x1980), self.data), '')
    
    def testConvertLongFirst(self):
        # convert longer match first
        # 123: A,1234: Z
        # 1234 => Z... not A4
        data = (({"0":"X"}, {"09":"M"}, {"123":"A"}, {"1234":"Z"}) , [])
        # dictionary not in unicode range
		# list with character replacement values

        self.assertEqual(converter("1234", data), "Z")
        

if __name__ == '__main__':
    unittest.main()
