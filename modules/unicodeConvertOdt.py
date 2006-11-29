#!/usr/bin/python
# -*- coding: utf8 -*-

# Khmer Legacy fonts to Khmer Unicode Conversion
# (c) 2006 Open Forum of Cambodia, all rights reserved.
#
# # Version 1.0 (10 June 2006)
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

def convertOdtFile(inputFileName, outputFileName, outputFont = None, outputFontSize = None):
    """
    This function convert OpenOffice.Org writer file
    inputFileName: the name of file you want to convert. 
    outputFileName: the result file name. Default value is converted-inputFileName
    outputFont: font name to override. default value is Khmer OS.
    outputFontSize: a value to override font size in odt file, value = None to ignore.
    """    
        
    CONTENTXML = 'content.xml'
    STYLESXML = 'styles.xml'

    if (inputFileName == outputFileName):
        raise TypeError('input file and output file must be different!')

    try:
        # read zip file (.odt)
        zipIn = zipfile.ZipFile(inputFileName, "r")
    except IOError:        
        raise IOError('Cannot open file "' +  inputFileName + '" for reading!')

    if (not (CONTENTXML and STYLESXML) in zipIn.namelist()):        
        raise TypeError('Input file' + inputFileName + 'is not an odt file!')
    
    try:
        # create new zip file (.odt)
        zipOut = zipfile.ZipFile(outputFileName, "w", DEFLATED)
    except IOError:        
        raise IOError('Cannot open file "' +  outputFileName + '" for writing!')

    styleReplace = {}
    zipOut.debug = 3
    for file in zipIn.namelist():
        fdata = zipIn.read(file)
        if (file == CONTENTXML):
            # read data to contentXml for later processing.
            contentXml = fdata
            continue
        elif (file == STYLESXML):
            fdata, style = modifyStyle(fdata, outputFont, outputFontSize)
            # get style name that need to convert to unicode inside style.xml.
            styleReplace.update(style)
        zipOut.writestr(file, fdata)

    # process the content.xml only after already read the styles.xml.
    fdata = xmlProcess(contentXml, outputFont, outputFontSize, styleReplace)
    zipOut.writestr(CONTENTXML, fdata)
    zipOut.close()
    zipIn.close()

def xmlProcess(xmldata, fontNameReplace = "Khmer OS", fontSizeReplace = None, styleReplace = None):
    """
    input: xml data string
    return: xml data string in utf-8 encoding where text is converted
    """
    xmldoc = minidom.parseString(xmldata)
    officeNode = xmldoc.getElementsByTagName('office:text')
    fontNode = xmldoc.getElementsByTagName('office:font-face-decls')
    
    fd = FontData()
    if (fontSizeReplace):
        fontSizeReplace = str(fontSizeReplace) + 'pt'
  
    def goThru (nodelist):
        """
        go through all nodes and execute the convertIfLegacy() on every nodes
        """
        for node in nodelist:
            if node.hasChildNodes():
                for child in node.childNodes:
                    convertIfLegacy(child)
                goThru (node.childNodes)

    def convertIfLegacy(node):
        """look the node for information of legacy font and convert to unicode, otherwise return False.
        @param node: node to look to and convert if necessary."""
        if (not node.nodeValue):
            return False
        try:
            stylename = node.parentNode.getAttribute(u'text:style-name')
            if (not stylename in style):
                return False
        except:
            return False
        #legacy font data's referal.
        fontname = style[stylename]
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
                        part = unicodeProcess.process(part, fd.legacyData(fontname))
                        result += unicodeReorder.reorder(part)
                        part = ''
                    result += char
                else:
                    part += tmpChar
                    
            if (part):
                part = unicodeProcess.process(part, fd.legacyData(fontname))
                result += unicodeReorder.reorder(part)
            sin = result
        else:
            sin = unicodeProcess.process(sin, fd.legacyData(fontname))
            sin = unicodeReorder.reorder(sin)
        
        newtext = xmldoc.createTextNode(sin) # create text of Node
        node.parentNode.replaceChild(newtext, node)

    def updateStyle(style = {}):
        """get style name (in xmldoc) that need to convert to unicode, update font name and size,
        And return style.
        @param style: style indicates that the node has to convert to unicode."""
        styleNode = xmldoc.getElementsByTagName('style:style')
        if (len(styleNode) == 0):
            # create parent node for style node
            styleNodeParent = xmldoc.getElementsByTagName('office:automatic-styles')[0]
            styleNode = xmldoc.createElement('style:style')
            styleNodeParent.appendChild(styleNode)
            styleNode = xmldoc.getElementsByTagName('style:style')
        for i in range(styleNode.length):
            newnode = styleNode[i]
            for j in range(len(newnode.childNodes)):
                name = newnode.childNodes[j].nodeName
                if (name == 'style:text-properties'):
                    try:
                        fonttype = newnode.childNodes[j].attributes['style:font-name'].nodeValue
                    except KeyError:
                        fonttype = ''
                    try:
                        fonttype = fd.typeForFontname(fonttype)
                    except fd.FontNotFoundError:
                        fonttype = ''
                    if (fd.defaultFont(fonttype)):
                        # add font to style list, only if it is convertible.
                        style[newnode.attributes['style:name'].nodeValue] = fonttype
                        # change font name and size in the xmldoc
                        newnode.childNodes[j].setAttribute('style:font-name-complex', fontNameReplace)
                        newnode.childNodes[j].setAttribute('style:font-name', fontNameReplace)
                        if (fontSizeReplace):
                            newnode.childNodes[j].setAttribute('style:font-size-complex', fontSizeReplace)
                            newnode.childNodes[j].setAttribute('style:font-size', fontSizeReplace)
        return style

    # get and update style in content.xml
    style = updateStyle(styleReplace)
    # go through all nodes and convert to unicode
    goThru(officeNode)
    return xmldoc.toxml('utf-8')

def modifyStyle(xmlData, targetFontName = "Khmer OS", targetFontSize = None):
    """change the "style:font-name" in "office:styles" of xmldata to fontNameReplace.
    Return a modified xml data encode in utf-8 and style as dictionary.
    @param xmldata input: xml data string.
    @param targetFontName (optional): font name to replace.
    @param targetFontSize (optional): font size to replace."""
    xmldoc = minidom.parseString(xmlData)
    officeStylesNode = xmldoc.getElementsByTagName('office:styles')[0]

    def modifyNode(nodelist):
        """go through all nodes and execute the replaceFont() on every nodes.
        @param nodelist: dom's node list."""
        for node in nodelist:
            if node.hasChildNodes():
                for child in node.childNodes:
                    replaceFont(child, targetFontName, targetFontSize)
                modifyNode(node.childNodes)
    
    def replaceFont(node, targetFontName, targetFontSize):
        """look for node which has "style:font-name" attribute and change its value to fontName.
        @param targetFontName: value to replace sourceFontName.
        @param targetFontSize: value to override in "style:font-size-asian"."""
        try:
            fontName = node.getAttribute(u'style:font-name')
            if (fontName):
                fonttype = fd.typeForFontname(fontName)
                if (fonttype):
                    # add name to convertible list...
                    style[unicode(node.parentNode.getAttribute(u'style:name'))] = fonttype
                    node.setAttribute(u'style:font-name', targetFontName)
                    if (fontSizeReplace != None):
                        node.setAttribute(u'style:font-size-asian', str(targetFontSize) + 'pt')
        except:
            pass

    fd = FontData()
    style = {}
    modifyNode(officeStylesNode.childNodes)
    return xmldoc.toxml('utf-8'), style
    
class TestConvertOdt(unittest.TestCase):
    def testSameFile(self):
        # same file raise error
        self.assertRaises(TypeError, convertOdtFile, 'file1', 'file1')

    def testUnreadable(self):
        # assert error if file is unreadable
        self.assertRaises(IOError, convertOdtFile, '!@#$%^&', 'file2')
        
    def testModifyStyle(self):
        xmldata = """<?xml version="1.0" encoding="UTF-8"?>
        <office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" office:version="1.0">
            <office:font-face-decls>
                <style:font-face style:name="Limon S1" svg:font-family="'Limon S1'" style:font-pitch="variable"/>
            </office:font-face-decls>
            <office:styles>
                <style:style style:name="Khmer" style:family="text" style:parent-style-name="Default_20_Paragraph_20_Font">
                    <style:text-properties style:font-name="Limon S1" fo:font-size="16pt" style:font-size-asian="16pt"/>
                </style:style>
            </office:styles>
            <office:automatic-styles></office:automatic-styles>
            <office:master-styles></office:master-styles>
        </office:document-styles>"""
        modxmldata = 'haha'
        self.assertEqual(modifyStyle(xmldata), modxmldata)

if __name__ == '__main__':

    xmldata = """<?xml version="1.0" encoding="UTF-8"?>
    <office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" xmlns:chart="urn:oasis:names:tc:opendocument:xmlns:chart:1.0" office:version="1.0">
        <office:font-face-decls>
            <style:font-face style:name="Limon S1" svg:font-family="'Limon S1'" style:font-pitch="variable"/>
        </office:font-face-decls>
        <office:styles>
            <style:style style:name="Khmer" style:family="text" style:parent-style-name="Default_20_Paragraph_20_Font">
                <style:text-properties style:font-name="Limon S1" fo:font-size="16pt" style:font-size-asian="16pt"/>
            </style:style>
        </office:styles>
        <office:automatic-styles></office:automatic-styles>
        <office:master-styles></office:master-styles>
    </office:document-styles>"""
    modifyStyle(xmldata)
    #unittest.main()
