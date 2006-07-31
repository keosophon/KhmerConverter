#!/usr/bin/python
# -*- coding: utf8 -*-

# Khmer Unicode to Legacy fonts Conversion
# (c) 2006 Open Forum of Cambodia, all rights reserved.
#
# Version 1.0 (10 June 2006)
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
# This module convertes an *.odt file from Unicode to  legacy Khmer format 

from xml.dom import minidom
from FontDataXML import FontData
import legacyReorder
import legacyConverter
import unittest
import zipfile
from zlib import DEFLATED

SP = unichr(0x20)
ZWSP = unichr(0x200B)
ZWNJ = unichr(0x200C)
ZWJ = unichr(0x200D)
INKHMER = SP + ZWSP + ZWNJ + ZWJ
STARTKHMER = u"«»" + ZWNJ + ZWSP + ZWJ
MINUNIC = 0x1780
MAXUNIC = 0x17FF

def convertOdtFile(inputFileName, outputFileName, outputFont, outputFontSize = None):
    """This function converts OpenOffice.org Writer file.
    inputFileName : name of input file to convert
    outputFileName : name of output file. Default value is converted-inputFileName.
    outputFont : legacy output font name. Default depends on the font type.
   outputFontSize : force the font size the output file will use. value = None to ignore.
    """
        
    CONTENTXML = 'content.xml'

    fd = FontData()
    if (not fd.isConvertable(outputFont)):
        raise TypeError('unknown output font ' + outputFont + '!')

    if (inputFileName == outputFileName):
        raise TypeError('input file and output file must be different!')

    try:
        # read zip file (.odt)
        zipIn = zipfile.ZipFile(inputFileName, "r")
    except IOError:
        raise IOError('Cannot open file "' +  inputFileName + '" for reading!')

    if (not CONTENTXML in zipIn.namelist()):        
        raise TypeError('Input file' + inputFileName + 'is not an odt file!')

    try:
        # create new zip file (.odt)
        zipOut = zipfile.ZipFile(outputFileName, "w", DEFLATED)
    except IOError:               
        raise IOError('Cannot open file "' +  outputFileName + '" for writing!')

    for file in zipIn.namelist():
        fdata = zipIn.read(file)
        # do the converting for content.xml only
        if (file == CONTENTXML):
            fdata = xmlProcess(fdata, outputFont, outputFontSize)
            # TODO: do we need to test the type? When do we not want to encode in UTF-8 ?
            if (type(fdata) == unicode):
                fdata = fdata.encode('utf-8')
        zipOut.writestr(file, fdata)

    zipOut.close()
    zipIn.close()


def xmlProcess(xmlData, fontNameReplace, fontSizeReplace = None):
    """
    input: xml data in unicode string
    return: xml data string in legacy encoding where text is converted
    """

    def goThru (node):
        """
        go through all nodes and execute the process() on every nodes
        """
        currNode = node
        while (currNode):
            if (currNode.hasChildNodes()):
                goThru(currNode.firstChild)
            currNode = process(currNode)
            currNode = currNode.nextSibling
    

    def process(node):
        """
        take Khmer Unicode data out of current node, convert it and put
        it in a new node which mark as Khmer.
        """
        if not node.nodeValue:
            return node
            
        sin = node.data
        newNode = xmldoc.createDocumentFragment()
        cursor = 0
        charCount = len(sin)
        while (cursor < charCount):
            khmStr = u''
            othStr = u''
            while (cursor < charCount):
                val = ord(sin[cursor])
                # in khmer range
                if ((val >= MINUNIC) and (val <= MAXUNIC)) or (STARTKHMER.find(unichr(val)) != -1) or (len(khmStr) > 0 and INKHMER.find(unichr(val)) != -1):
                    if (othStr):
                        break
                    khmStr += sin[cursor]
                # in other range
                else:
                    if (khmStr):
                        break
                    othStr += sin[cursor]
                cursor += 1
            # end of while (khmer string or other string found)

            if (khmStr):
                # convert khmer text
                khmStr = legacyReorder.reorder(khmStr)
                khmStr = legacyConverter.converter(khmStr, data)
                khmStr = khmStr.decode('cp1252')
                # add new khmer node
                khmNode = xmldoc.createElement('text:span')
                khmNode.setAttribute('text:style-name', 'khmerStyle')
                # add data
                txtNode = xmldoc.createTextNode(khmStr)
                khmNode.appendChild(txtNode)
                newNode.appendChild(khmNode)
            elif (othStr):
                txtNode = xmldoc.createTextNode(othStr)
                newNode.appendChild(txtNode)
                
        returnNode = newNode.lastChild
        node.parentNode.replaceChild(newNode, node)
        return returnNode

    xmldoc = minidom.parseString(xmlData)

    # get data for the font
    fd = FontData()
    data = fd.unicodeData(fontNameReplace)
    fontNameReplace = fd.defaultFont(fontNameReplace)
    
    # add font declaration
    newNode = xmldoc.createElement('style:font-face')
    newNode.setAttribute('style:name', fontNameReplace)
    newNode.setAttribute('svg:font-family', fontNameReplace)
    fontNodes = xmldoc.getElementsByTagName('office:font-face-decls')
    fontNodes[0].appendChild(newNode)

    # add font style
    newNode = xmldoc.createElement('style:style')
    newNode.setAttribute('style:family', 'text')
    newNode.setAttribute('style:name', 'khmerStyle')
    newNodeChild = xmldoc.createElement('style:text-properties')
    newNodeChild.setAttribute('style:font-name', fontNameReplace)
    if (fontSizeReplace):
        fontSizeReplace = str(fontSizeReplace) + 'pt'
        newNodeChild.setAttribute('fo:font-size', fontSizeReplace)
    newNode.appendChild(newNodeChild)
    styleNodeParent = xmldoc.getElementsByTagName('office:automatic-styles')[0]
    styleNodeParent.appendChild(newNode)

    # go through all nodes and convert to legacy
    officeNodes = xmldoc.getElementsByTagName('office:text')
    goThru(officeNodes[0])

    return xmldoc.toxml()
   

class TestConvertOdt(unittest.TestCase):

    def testSameFile(self):
        # same file raise error
        self.assertRaises(TypeError, convertOdtFile, 'file1', 'file1', 'abc')

    def testWrongFont(self):
        # same file raise error
        self.assertRaises(TypeError, convertOdtFile, 'file1', 'file2', 'fontTHATdoesNOTexist')

    def testOpenUnavailableFile(self):
        # raise error when file is unavailable
        self.assertRaises(IOError, convertOdtFile, 'AfileTHATdoesNOTexist', 'file1', 'abc')
    
    def testXmlProcess(self):
        myXml = u"""<?xml version="1.0" ?><office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"><office:font-face-decls/><office:automatic-styles/><office:body><office:text><text:p text:style-name="Standard">កខគabcច ឆ ជxyz</text:p></office:text></office:body></office:document-content>"""

        convertedXml = u"""<?xml version="1.0" ?><office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0"><office:font-face-decls><style:font-face style:name="ABC-TEXT-05" svg:font-family="ABC-TEXT-05"/></office:font-face-decls><office:automatic-styles><style:style style:family="text" style:name="khmerStyle"><style:text-properties style:font-name="ABC-TEXT-05"/></style:style></office:automatic-styles><office:body><office:text><text:p text:style-name="Standard"><text:span text:style-name="khmerStyle">kxK</text:span>abc<text:span text:style-name="khmerStyle">c q C</text:span>xyz</text:p></office:text></office:body></office:document-content>"""

        self.assertEqual(xmlProcess(myXml.encode('utf-8'), 'ABC-TEXT-05'), convertedXml)

if __name__ == '__main__':
    unittest.main()
