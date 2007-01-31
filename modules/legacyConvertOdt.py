#!/usr/bin/python
# -*- coding: utf8 -*-

# Khmer Unicode to Legacy fonts Conversion
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
KHMERSTYLE = 'kc-1.0-kstyle'

class legacyConvertOdt:
    def __init__(self):
        self.CONTENTXML = 'content.xml'
        self.STYLESXML = 'styles.xml'
        self.fd = FontData()
        self.outputFont = "ABC-TEXT-05"
        self.outputFontSize = None
        self.data = self.fd.unicodeData(self.outputFont)

    def convertOdtFile(self, inputFileName, outputFileName, outputFont, outputFontSize = None):
        """This function converts OpenOffice.org Writer file.
        inputFileName : name of input file to convert
        outputFileName : name of output file. Default value is converted-inputFileName.
        outputFont : legacy output font name. Default depends on the font type.
        outputFontSize : force the font size the output file will use. value = None to ignore.
        """
        if (not self.fd.isConvertable(outputFont)):
            raise TypeError('unknown output font ' + outputFont + '!')
    
        if (inputFileName == outputFileName):
            raise TypeError('input file and output file must be different!')
    
        try:
            # read zip file (.odt)
            zipIn = zipfile.ZipFile(inputFileName, "r")
        except IOError:
            raise IOError('Cannot open file "' +  inputFileName + '" for reading!')
    
        if (not (self.CONTENTXML and self.STYLESXML) in zipIn.namelist()):        
            raise TypeError('Input file' + inputFileName + 'is not an odt file!')
    
        try:
            # create new zip file (.odt)
            zipOut = zipfile.ZipFile(outputFileName, "w", DEFLATED)
        except IOError:               
            raise IOError('Cannot open file "' +  outputFileName + '" for writing!')
        
        # get data for the font
        self.outputFont = self.fd.defaultFont(outputFont)
        self.data = self.fd.unicodeData(self.outputFont)
        if (outputFontSize):
            self.outputFontSize = str(outputFontSize) + 'pt'
        
        for file in zipIn.namelist():
            fdata = zipIn.read(file)
            # do the converting for content.xml only
            if (file == self.CONTENTXML):
                fdata = self.processContent(fdata)
                # TODO: do we need to test the type? When do we not want to encode in UTF-8 ?
                if (type(fdata) == unicode):
                    fdata = fdata.encode('utf-8')
            elif (file == self.STYLESXML):
                fdata = self.processStyle(fdata)
                # TODO: do we need to test the type? When do we not want to encode in UTF-8 ?
                if (type(fdata) == unicode):
                    fdata = fdata.encode('utf-8')
            zipOut.writestr(file, fdata)
        zipOut.close()
        zipIn.close()
    
    def processContent(self, xmlData):
        """
        input: xml data in unicode string
        return: xml data string in legacy encoding where text is converted
        """
        self.xmldoc = minidom.parseString(xmlData)
        
        officeNode = self.xmldoc.getElementsByTagName('office:text')
        officeAutoStylesNode = self.xmldoc.getElementsByTagName('office:automatic-styles')[0]
        officeFontFaceDecls = self.xmldoc.getElementsByTagName('office:font-face-decls')[0]
        # add font information
        self.addFontInfo(officeAutoStylesNode, officeFontFaceDecls)
        # go through office node and convert to legacy.
        self.goThru(officeNode, self.convertIfUnicode)
        return self.xmldoc.toxml()
    
    def processStyle(self, xmldata):
        """change font name and size, convert data to legacy in xmldata
        @param xmldata: xml string to parse."""
        self.xmldoc = minidom.parseString(xmldata)
        officeAutoStylesNode = self.xmldoc.getElementsByTagName('office:automatic-styles')[0]
        officeFontFaceDecls = self.xmldoc.getElementsByTagName('office:font-face-decls')[0]
        officeMasterStylesNode = self.xmldoc.getElementsByTagName('office:master-styles')
        # go through node, replace font, and convert data to legacy.
        self.addFontInfo(officeAutoStylesNode, officeFontFaceDecls)
        self.goThru(officeMasterStylesNode, self.convertIfUnicode)
        return self.xmldoc.toxml('utf-8')
    
    def goThru (self, nodelist, function):
        """go through nodelist and call function with child node as argument.
        @param nodelist: dom's node list.
        @param function: function to call, child argument will be provided by goThru."""
        for node in nodelist:
            if node.hasChildNodes():
                for child in node.childNodes:
                    function(child)
                self.goThru (node.childNodes, function)
    
    def addFontInfo(self, autoStyleNode, declsNode):
        """add "style:style" to node."""
        # add font declaration
        styleFontFaceNode = self.xmldoc.createElement('style:font-face')
        styleFontFaceNode.setAttribute('style:name', self.outputFont)
        styleFontFaceNode.setAttribute('svg:font-family', self.outputFont)
        declsNode.appendChild(styleFontFaceNode)
    
        # add font style
        styleNode = self.xmldoc.createElement('style:style')
        styleNode.setAttribute('style:family', 'text')
        styleNode.setAttribute('style:name', KHMERSTYLE)
        styleTextPropNode = self.xmldoc.createElement('style:text-properties')
        styleTextPropNode.setAttribute('style:font-name', self.outputFont)
        if (self.outputFontSize):
            styleTextPropNode.setAttribute('fo:font-size', self.outputFontSize)
        styleNode.appendChild(styleTextPropNode)
        autoStyleNode.appendChild(styleNode)
    
    def convertIfUnicode(self, node):
        """
        take Khmer Unicode data out of current node, convert it and put
        it in a new node which mark as khmerConverter_DefaultStyle.
        """
        if not node.nodeValue:
            return node
        sin = node.data
        newNode = self.xmldoc.createDocumentFragment()
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
                khmStr = legacyConverter.converter(khmStr, self.data)
                khmStr = khmStr.decode('cp1252')
                # add new khmer node
                khmNode = self.xmldoc.createElement('text:span')
                khmNode.setAttribute('text:style-name', KHMERSTYLE)
                # add data
                txtNode = self.xmldoc.createTextNode(khmStr)
                khmNode.appendChild(txtNode)
                newNode.appendChild(khmNode)
            elif (othStr):
                txtNode = self.xmldoc.createTextNode(othStr)
                newNode.appendChild(txtNode)
                
        node.parentNode.replaceChild(newNode, node)

class TestConvertOdt(unittest.TestCase):
    def testSameFile(self):
        # same file raise error
        self.assertRaises(TypeError, legacyConvertOdt().convertOdtFile, 'file1', 'file1', 'abc')

    def testWrongFont(self):
        # same file raise error
        self.assertRaises(TypeError, legacyConvertOdt().convertOdtFile, 'file1', 'file2', 'fontTHATdoesNOTexist')

    def testOpenUnavailableFile(self):
        # raise error when file is unavailable
        self.assertRaises(IOError, legacyConvertOdt().convertOdtFile, 'AfileTHATdoesNOTexist', 'file1', 'abc')
    
    def testProcessContent(self):
        header = u"<?xml version=\"1.0\" ?><office:document-content xmlns:office=\"urn:oasis:names:tc:opendocument:xmlns:office:1.0\" xmlns:text=\"urn:oasis:names:tc:opendocument:xmlns:text:1.0\">"
        fontDeclOpen = u"<office:font-face-decls>"
        fontDeclClose = u"</office:font-face-decls>"
        autoStyleOpen = u"<office:automatic-styles>"
        autoStyleClose = u"</office:automatic-styles>"
        contentOpen = u"<office:body><office:text><text:p text:style-name=\"Standard\">"
        contentClose = u"</text:p></office:text></office:body></office:document-content>"

        myXml = header + \
            fontDeclOpen + fontDeclClose + \
            autoStyleOpen + autoStyleClose + \
            contentOpen + \
            "កខគabcច ឆ ជxyz" + \
            contentClose
        
        convertedXml = header + \
            fontDeclOpen + \
            u"<style:font-face style:name=\"ABC-TEXT-05\" svg:font-family=\"ABC-TEXT-05\"/>" + \
            fontDeclClose + \
            autoStyleOpen + \
            "<style:style style:family=\"text\" style:name=\"" + KHMERSTYLE + "\"><style:text-properties style:font-name=\"ABC-TEXT-05\"/></style:style>" + \
            autoStyleClose + \
            contentOpen + \
            "<text:span text:style-name=\"" + KHMERSTYLE + "\">kxK</text:span>abc<text:span text:style-name=\"" + KHMERSTYLE + "\">c q C</text:span>xyz" + \
            contentClose
        
        self.assertEqual(legacyConvertOdt().processContent(myXml.encode('utf-8')), convertedXml)

if __name__ == '__main__':
    unittest.main()
