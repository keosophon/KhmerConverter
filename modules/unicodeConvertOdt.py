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

    zipOut.debug = 3
    for file in zipIn.namelist():
        fdata = zipIn.read(file)
        # do the converting for content.xml only
        if (file == CONTENTXML):
            fdata = xmlProcess(fdata, outputFont, outputFontSize)
        zipOut.writestr(file, fdata)

    zipOut.close()
    zipIn.close()


def xmlProcess(xmldata, fontNameReplace = "Khmer OS", fontSizeReplace = None):
    """
    input: xml data string
    return: xml data string in utf-8 encoding where text is converted
    """
    xmldoc = minidom.parseString(xmldata)
    officeNode = xmldoc.getElementsByTagName('office:text')
    styleNode = xmldoc.getElementsByTagName('style:style')
    fontNode = xmldoc.getElementsByTagName('office:font-face-decls')
    
    if (len(styleNode) == 0):
        # create parent node for style node
        styleNodeParent = xmldoc.getElementsByTagName('office:automatic-styles')[0]
        styleNode = xmldoc.createElement('style:style')
        styleNodeParent.appendChild(styleNode)
        styleNode = xmldoc.getElementsByTagName('style:style')

    fd = FontData()    
    if (fontSizeReplace):
        fontSizeReplace = str(fontSizeReplace) + 'pt'
  
    def goThru (nodelist):
        """
        go through all nodes and execute the domycode() on every nodes
        """
        for node in nodelist:
            if node.hasChildNodes():
                for child in node.childNodes:
                    domycode (child)
                goThru (node.childNodes)

    def domycode (node):
        """
        look for node that use font in FontData and execute convert()
        """
        if (node.parentNode.attributes.keys() == [u'text:style-name']):
            stylename = node.parentNode.attributes[u'text:style-name'].nodeValue
            if stylename in style:
                if (fd.defaultFont(style[stylename])):
                    # convert Khmer legacy text into Unicode
                    convert(node, style[stylename])

    def convert(node, fontname):
        """
        Convert each node that has data to Unicode.
        """
        if node.nodeValue:
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

    # get style (font that need to convert to unicode)
    # change legacy font to Khmer OS and reduce size to 10
    style = {}
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
                # add font to style list
                style[newnode.attributes['style:name'].nodeValue] = fonttype
                if (fd.defaultFont(fonttype)):
                    # change font name and size
                    newnode.childNodes[j].setAttribute('style:font-name-complex', fontNameReplace)
                    newnode.childNodes[j].setAttribute('style:font-name', fontNameReplace)
                    if (fontSizeReplace):
                        newnode.childNodes[j].setAttribute('style:font-size-complex', fontSizeReplace)
                        newnode.childNodes[j].setAttribute('style:font-size', fontSizeReplace)

    # go through all nodes and convert to unicode
    goThru(officeNode)
    return xmldoc.toxml('utf-8')

class TestConvertOdt(unittest.TestCase):
    def testSameFile(self):
        # same file raise error
        self.assertRaises(TypeError, convertOdtFile, 'file1', 'file1')

    def testUnreadable(self):
        # assert error if file is unreadable
        self.assertRaises(IOError, convertOdtFile, '!@#$%^&', 'file2')

if __name__ == '__main__':
    unittest.main()
