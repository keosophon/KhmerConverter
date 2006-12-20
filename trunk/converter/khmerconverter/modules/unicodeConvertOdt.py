#!/usr/bin/python
# -*- coding: utf8 -*-

# Khmer Legacy fonts to Khmer Unicode Conversion
# (c) 2006 The WordForge Foundation, all rights reserved.
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
# This module convertes an *.odt file from legacy Khmer to Unicode format 

from xml.dom import minidom
from FontDataXML import FontData
import zipfile
import unicodeProcess
import unicodeReorder
import unittest
from zlib import DEFLATED

class unicodeConvertOdt:
    def __init__(self):
        self.CONTENTXML = 'content.xml'
        self.STYLESXML = 'styles.xml'
        self.convertibleStyle = {}
        self.fd = FontData()
        self.outputFont = "Khmer OS"
        self.outputFontSize = None

    def convertOdtFile(self, inputFileName, outputFileName, outputFont = None, outputFontSize = None):
        """This function convert OpenOffice.Org writer file
        inputFileName: the name of file you want to convert. 
        outputFileName: the result file name. Default value is converted-inputFileName
        outputFont: font name to override. default value is Khmer OS.
        outputFontSize: a value to override font size in odt file, value = None to ignore."""
        
        self.outputFont = outputFont
        if (outputFontSize):
            self.outputFontSize = str(outputFontSize) + 'pt'
        
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
    
        zipOut.debug = 3
        for file in zipIn.namelist():
            fdata = zipIn.read(file)
            if (file == self.CONTENTXML):
                # read data to contentXml for later processing.
                contentXml = fdata
                continue
            elif (file == self.STYLESXML):
                fdata = self.processStyle(fdata)
            zipOut.writestr(file, fdata)
    
        # process the content.xml only after already read the styles.xml.
        fdata = self.processContent(contentXml)
        zipOut.writestr(self.CONTENTXML, fdata)
        zipOut.close()
        zipIn.close()
    
    def processContent(self, xmldata):
        """change font name and size, convert data to unicode in xmldata
        @param xmldata: xml string to parse."""
        self.xmldoc = minidom.parseString(xmldata)
        officeNode = self.xmldoc.getElementsByTagName('office:text')
        officeDocContentNode = self.xmldoc.getElementsByTagName('office:document-content')
        # go through node, replace font, and convert data to unicode.
        self.goThru(officeDocContentNode, self.replaceFont)
        self.goThru(officeNode, self.convertIfLegacy)
        return self.xmldoc.toxml('utf-8')
    
    def processStyle(self, xmldata):
        """change font name and size, convert data to unicode in xmldata
        @param xmldata: xml string to parse."""
        self.xmldoc = minidom.parseString(xmldata)
        officeDocStylesNode = self.xmldoc.getElementsByTagName('office:document-styles')
        # go through node, replace font, and convert data to unicode.
        self.goThru(officeDocStylesNode, self.replaceFont)
        self.goThru(officeDocStylesNode, self.convertIfLegacy)
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
    
    def replaceFont(self, node):
        """look for node which has "style:font-name" attribute and change its value to fontName."""
        try:
            fontName = node.getAttribute('style:font-name')
            if (fontName):
                fontType = self.fd.typeForFontname(fontName)
                # add name to convertible list
                self.convertibleStyle[unicode(node.parentNode.getAttribute('style:name'))] = fontType
                node.removeAttribute('style:font-name')
                node.setAttribute('style:font-name-complex', self.outputFont)
                if (self.outputFontSize):
                    node.setAttribute('style:font-size-complex', self.outputFontSize)
        except:
            pass
            
        try:
            styleName = node.getAttribute('style:name')
            if (styleName):
                # if node's parent style is also convertible, node is also convertible.
                if (node.hasAttribute('style:parent-style-name')):
                    ParentStyleName = node.getAttribute('style:parent-style-name')
                    if self.convertibleStyle.has_key(ParentStyleName):
                        # add to convertible style
                        self.convertibleStyle[styleName] = self.convertibleStyle[ParentStyleName]
                fontType = self.fd.typeForFontname(styleName)
                self.convertibleStyle[styleName] = fontType
                node.setAttribute('style:name', self.outputFont)
                node.setAttribute('svg:font-family', self.outputFont)
        except:
            pass

    def convertIfLegacy(self, node):
        """look the node for information of legacy font and convert to unicode, otherwise return False.
        @param node: node to look to and convert if necessary."""
        if (not node.nodeValue):
            return False
        try:
            stylename = node.parentNode.getAttribute(u'text:style-name')
            if (not stylename in self.convertibleStyle):
                return False
        except:
            return False
        # legacy font data's referal.
        fontname = self.convertibleStyle[stylename]
        sin = node.data
        try:
            sin = sin.encode('cp1252')
        except UnicodeEncodeError:
            result = u''
            part = ''
            for char in sin:
                try:
                    tmpChar = char.encode('cp1252')
                except UnicodeEncodeError:
                    if (part):
                        part = unicodeProcess.process(part, self.fd.legacyData(fontname))
                        result += unicodeReorder.reorder(part)
                        part = ''
                    result += char
                else:
                    part += tmpChar
            if (part):
                part = unicodeProcess.process(part, self.fd.legacyData(fontname))
                result += unicodeReorder.reorder(part)
            sin = result
        else:
            sin = unicodeProcess.process(sin, self.fd.legacyData(fontname))
            sin = unicodeReorder.reorder(sin)
        newtext = self.xmldoc.createTextNode(sin) # create text of Node
        node.parentNode.replaceChild(newtext, node)


class TestConvertOdt(unittest.TestCase):
    def testSameFile(self):
        # same file raise error
        self.assertRaises(TypeError, unicodeConvertOdt().convertOdtFile, 'file1', 'file1')

    def testUnreadable(self):
        # assert error if file is unreadable
        self.assertRaises(IOError, unicodeConvertOdt().convertOdtFile, '!@#$%^&', 'file2')
        
    def testModifyStyle(self):
        xmldata = """<?xml version="1.0" encoding="utf-8"?>
<office:document-styles office:version="1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0"><office:font-face-decls><style:font-face style:font-pitch="variable" style:name="Limon S1" svg:font-family="Limon S1"/></office:font-face-decls><office:styles><style:style style:family="text" style:name="Khmer" style:parent-style-name="Default_20_Paragraph_20_Font"><style:text-properties fo:font-size="16pt" style:font-name="Limon S1" style:font-size-asian="16pt"/></style:style></office:styles><office:automatic-styles/><office:master-styles/></office:document-styles>"""
        modxmldata = xmldata.replace("Limon S1", "Khmer OS")
        modxmldata = modxmldata.replace("style:font-name", "style:font-name-complex")
        self.assertEqual(unicodeConvertOdt().processStyle(xmldata), modxmldata)

if __name__ == '__main__':
    unittest.main()
