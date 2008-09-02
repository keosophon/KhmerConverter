#!/usr/bin/python
# -*- coding: utf-8 -*-
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
# This module is working on the khmer converter graphical interface using Qt

import os, sys
from PyQt4 import QtCore, QtGui
from Ui_KConverter import Ui_kconvert
from FontDataXML import FontData
from mimetypes import MimeTypes
from AboutKConvert import AboutKConvert
import __version__

class Kconvert(QtGui.QMainWindow):
    """
    The main window which holds the toolviews.
    """

    def __init__(self, parent = None):
        QtGui.QMainWindow.__init__(self, parent)
        self.ui = Ui_kconvert()
        self.ui.setupUi(self)

        self.tab = "Leg"
        self.originExt = ".txt"
        settingOrg = "KhmerConverter"
        settingApp = "Khmer Converter"
        self.settings = QtCore.QSettings(QtCore.QSettings.IniFormat, QtCore.QSettings.UserScope,settingOrg, settingApp)

        self.setWindowTitle(settingApp + ' ' + __version__.ver)
        
        self.connect(self.ui.tabWidget, QtCore.SIGNAL("currentChanged(int)"), self.tabChanged)
        
        #---------------------------------------Legacy to Unicode------------------------------------------
        # legacy to Unicode --  signal for browsing folder
        self.connect(self.ui.btnBrowseInL, QtCore.SIGNAL("clicked()"), self.openDialog)
        self.connect(self.ui.btnBrowseOutL, QtCore.SIGNAL("clicked()"), self.saveDialog)
        self.connect(self.ui.cmbDocTypeL, QtCore.SIGNAL("currentIndexChanged(QString)"), self.docTypeChangedL)
        self.connect(self.ui.cmbDocTypeU, QtCore.SIGNAL("currentIndexChanged(QString)"), self.docTypeChangedU)
        
        # add items into combo box doctType for legacy
        self.typeOdt = "OpenOffice.org Writer (*.odt)"
        self.typeText = "Plain Text"
        self.typeHtml = "Web page, HTML"
        self.docTypes = [self.typeOdt, self.typeText, self.typeHtml]
        for doctType in self.docTypes:
            self.ui.cmbDocTypeL.addItem(self.tr(doctType))
            
        # add items into combo box legacy font for legacy
        for font in FontData().listFontTypes():
            self.ui.cmbFontInputL.addItem(font)
            for fontName in FontData().listFontNamesForType(font):
                self.ui.cmbFontInputL.addItem("  " + fontName)
                
        # add items into combo box unicode font for legacy
        self.unicodeFontList = ['Khmer OS', 'Khmer OS Bokor', 'Khmer OS Battambang', 'Khmer OS Content', 'Khmer OS Fasthand', 'Khmer OS Freehand','Khmer OS Metal Chrieng', 'Khmer OS Muol', 'Khmer OS Muol Light', 'Khmer OS Muol Pali', 'Khmer OS SiemReap', 'Khmer OS System']

        for i in self.unicodeFontList:
            self.ui.cmbFontOutputL.addItem(i)
         
        self.defaultUniFont()
        
        # add items into combo box ecoding for legacy
        self.encodings = {"Plain Text (cp1252)":'cp1252',  "Plain Text (latin-1/iso-8859-1)":'iso-8859-1', "Unicode (utf-8)":'utf-8'}
        for key in self.encodings:
            self.ui.cmbEncodingL.addItem(self.tr(key))
            
        self.connect(self.ui.lineInputL, QtCore.SIGNAL("textChanged(QString)"), self.detectDocType)
        self.connect(self.ui.chbOverrideSizeL, QtCore.SIGNAL("stateChanged(int)"), self.toggleSize)
        
        #---------------------------------------Unicode to Legacy------------------------------------------
        # unicode to legacy --  signal for browsing folder
        self.connect(self.ui.btnBrowseInU, QtCore.SIGNAL("clicked()"), self.openDialog)
        self.connect(self.ui.btnBrowseOutU, QtCore.SIGNAL("clicked()"), self.saveDialog)
        
        # add item into combo box doctType for unicode
        for doctType in self.docTypes:
            self.ui.cmbDocTypeU.addItem(self.tr(doctType))

        # add items into combo box legacy font for unicode
        self.legacyFontList = []
        for font in FontData().listFontTypes():
            self.ui.cmbFontOutputU.addItem(font)
            self.legacyFontList.append(font)
            for fontName in FontData().listFontNamesForType(font):
                self.ui.cmbFontOutputU.addItem("  " + fontName)
                self.legacyFontList.append(fontName)
        
        self.defaultLegFont()
                
        self.connect(self.ui.lineInputU, QtCore.SIGNAL("textChanged(QString)"), self.detectDocType)
        self.connect(self.ui.chbOverrideSizeU, QtCore.SIGNAL("stateChanged(int)"), self.toggleSize)
        
        # menubar
        self.connect(self.ui.actionQuit,  QtCore.SIGNAL("triggered()"), QtCore.SLOT("close()"))
        self.connect(self.ui.actionAboutQt, QtCore.SIGNAL("triggered()"), QtGui.qApp, QtCore.SLOT("aboutQt()"))
        
        # Help menu
        self.aboutKConvert = AboutKConvert(self)
        self.connect(self.ui.actionAboutKConverter, QtCore.SIGNAL("triggered()"), self.aboutKConvert.showDialog)
        
        # set default value
        self.defaultValue()
        
        # instance of mime type
        self.mt = MimeTypes()
        
        self.connect(self.ui.btnConvert, QtCore.SIGNAL("clicked()"), self.convert)
        self.connect(self.ui.btnReset, QtCore.SIGNAL("clicked()"), self.defaultValue)
    
    def defaultUniFont(self):   
        # get index for khmeros
        INDEXKHMEROS = 0
        for i in range(len(self.unicodeFontList)):
            if (self.unicodeFontList[i] == 'Khmer OS'):
                INDEXKHMEROS = i
                break
        self.ui.cmbFontOutputL.setCurrentIndex(INDEXKHMEROS)
    
    def defaultLegFont(self):
        # get index for abc-zwsp
        INDEXABCZWSP = 0
        for i in range(len(self.legacyFontList)):
            if (self.legacyFontList[i] == 'abc-zwsp'):
                INDEXABCZWSP = i
                break
        self.ui.cmbFontOutputU.setCurrentIndex(INDEXABCZWSP)
        self.ui.cmbFontInputL.setCurrentIndex(INDEXABCZWSP)
        
    def tabChanged(self, curIndex):
        """
        Dectect which tab is active.
        """
        if (curIndex == 0):
            self.tab = "Leg"
        else:
            self.tab = "Uni"
        
    def defaultValue(self):
        """
        Set default view and directory
        """
        
        self.ui.lineInputL.setText("")
        self.ui.lineInputU.setText("")
        self.ui.lineOutputL.setText("")
        self.ui.lineOutputU.setText("")
        
        self.defaultUniFont()
        self.defaultLegFont()
        self.ui.cmbEncodingL.setCurrentIndex(0)
        self.ui.cmbDocTypeL.setCurrentIndex(0)
        self.ui.cmbDocTypeU.setCurrentIndex(0)
        self.ui.chbOverrideSizeL.setChecked(False)
        self.ui.chbOverrideSizeU.setChecked(False)
        self.ui.spinBoxSizeL.setValue(11)
        self.ui.spinBoxSizeU.setValue(20)
        
        
        # default value for directory for file selection dialog
        self.directory = self.settings.value("workingDir").toString()
        if (not self.directory) or (not os.path.exists(self.directory)):
            self.directory = QtCore.QDir.homePath()
    
    def docTypeChangedL(self, text):
        if (text == self.typeOdt):
            self.ui.chbOverrideSizeL.setEnabled(True)
            self.ui.cmbFontInputL.setEnabled(False)
            self.ui.cmbEncodingL.setEnabled(False)
            self.ui.cmbFontOutputL.setEnabled(True)
            
        else:
            self.ui.chbOverrideSizeL.setEnabled(False)
            self.ui.cmbFontInputL.setEnabled(True)
            self.ui.cmbEncodingL.setEnabled(True)
            self.ui.cmbFontOutputL.setEnabled(False)
    
    def docTypeChangedU(self, text):
        if (text == self.typeOdt):
            self.ui.chbOverrideSizeU.setEnabled(True)
        else:
            self.ui.chbOverrideSizeU.setEnabled(False)
    
    def openDialog(self):
        """
        Open an open file selection dialog
        """
        directory = self.settings.value("workingDir").toString()
        filename = QtGui.QFileDialog.getOpenFileName(self, self.tr("Open File"),
                        directory,
                        self.tr("All Files (*);;OpenOffice.org Writer(*.odt);;Plain Text (*.txt);;Web page, HTML(*.html *.htm)"))
        if (filename.isEmpty()):
            return False
        else:
            if (self.tab == "Leg"):
                self.setPath(filename, self.ui.lineInputL, self.ui.lineOutputL)
            else:
                self.setPath(filename, self.ui.lineInputU, self.ui.lineOutputU)
            return True
            
    def setPath(self, filename, objIn, objOut):
        """
        Set filepath to the control
        
        @param filename: a filepath to put in control
        @param objIn: the control for input file
        @param objOut: the control for output file
        """
        objIn.setText(filename)
        directory = os.path.dirname(unicode(filename))
        self.settings.setValue("workingDir", QtCore.QVariant(directory))
    
        # output font 
        path, name = os.path.split(unicode(filename))
        filename = os.path.join(path, 'converted-' + name)
        objOut.setEnabled(True)
        objOut.setText(filename)
        self.emit(QtCore.SIGNAL("filename"), unicode(filename))

    def saveDialog(self):
        """
        Open a save dialog.
        """
        directory = self.settings.value("workingDir").toString()
        filename = QtGui.QFileDialog.getSaveFileName(self,
                    self.tr("Save File As"),
                    directory,
                    self.tr("All Files (*);;OpenOffice.org Writer(*.odt);;Plain Text (*.txt);;Web page, HTML(*.html *.htm)"))
        if (filename):
            print "input", type(filename)
            name, ext = os.path.splitext(unicode(filename))
            if (self.originExt == ".txt"):
                filename = filename + ".txt"
            elif (self.originExt == ".odt"):
                filename = filename + ".odt"
            elif (self.originExt == ".html") or (self.originExt == ".htm"):
                filename = filename + ".htm"
            if (self.tab == "Leg"):
                self.ui.lineOutputL.setText(filename)
            else:
                self.ui.lineOutputU.setText(filename)
            print "output", type(filename)
            directory = os.path.dirname(unicode(filename))
            self.settings.setValue("workingDir", QtCore.QVariant(directory))
            
    def setDocType(self, filename, obj):
        """
            set document type of filename to the obj.
        """
        filename = unicode(filename)
        if (os.path.isfile(filename)):
            mimeType = self.mt.guess_type(filename)[0]
            if (mimeType == 'application/vnd.oasis.opendocument.text'):
                obj.setCurrentIndex(0)
                fileExtension = ".odt"
            elif (mimeType == 'text/html' or mimeType == 'text/xml'):
                obj.setCurrentIndex(2)
                fileExtension = ".html"
            elif (mimeType == None):
                # if mimeType failed to give apropriet value, use file
                # extension instead.
                name, ext = os.path.splitext(filename)
                ext = ext[len(os.path.extsep):].lower()
                fileExtension = "." + ext
                if (fileExtension == ".odt"):
                    obj.setCurrentIndex(0)
                elif (fileExtension == ".html") or (fileExtension == ".htm"):
                    obj.setCurrentIndex(2)
                else:
                    obj.setCurrentIndex(1)
            else:
                obj.setCurrentIndex(1)
                fileExtension = ".txt"
        else:
            fileExtension = ".txt"
        self.originExt = fileExtension

    def detectDocType(self, filename):
        """
        Dectect the document type of input filename.
        """
        if (self.tab == "Leg"):
            self.setDocType(filename, self.ui.cmbDocTypeL)
        else:
            self.setDocType(filename, self.ui.cmbDocTypeU)
    
    def toggleSize(self):
        """
        Enable or disable size label and spin box.
        """
        if (self.tab == "Leg"):
            objLbl = self.ui.lblSizeL
            objSpin = self.ui.spinBoxSizeL
        else:
            objLbl = self.ui.lblSizeU
            objSpin = self.ui.spinBoxSizeU
            
        if (isinstance(self.sender(), QtGui.QCheckBox)):
            checked = self.sender().isChecked()
            if (checked):
                objLbl.setEnabled(True)
                objSpin.setEnabled(True)
            else:
                objLbl.setEnabled(False)
                objSpin.setEnabled(False)
        
    def convert(self):
        """
        A function interface to convert between format.
        """
        self.ui.btnConvert.setFocus()
        if (self.tab == "Leg"):
            objDocType = self.ui.cmbDocTypeL
            objEncoding = self.ui.cmbEncodingL
            objFontIn = self.ui.cmbFontInputL
            objFontOut = self.ui.cmbFontOutputL
            objSpinSize = self.ui.spinBoxSizeL
            objLineIn = self.ui.lineInputL
            objLineOut = self.ui.lineOutputL
            encoding = objEncoding.currentText()
            encoding = self.encodings[str(encoding)]
        else:
            objDocType = self.ui.cmbDocTypeU
            objFontOut = self.ui.cmbFontOutputU
            objSpinSize = self.ui.spinBoxSizeU
            objLineIn = self.ui.lineInputU
            objLineOut = self.ui.lineOutputU
        docType = objDocType.currentText()

        # output font is priority
        if (objFontOut.isEnabled()):
            font = str(objFontOut.currentText()).strip()
        else:
            font = str(objFontIn.currentText()).strip()

        # set font size to zero if it is disabled
        if objSpinSize.isEnabled():
            fontSize = objSpinSize.value()
        else:
            fontSize = None
        
        inputFile = str(objLineIn.text())
        outputFile = str(objLineOut.text())

        # check if output file already exist
        if (os.path.exists(outputFile)):
            confirm = QtGui.QMessageBox.question(self, self.tr("Warning"), 
                "The output file does already exist!\n\nDo you want to overwrite?",
                QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default, 
                QtGui.QMessageBox.No | QtGui.QMessageBox.Escape) 
            if (confirm == QtGui.QMessageBox.No):
                return
            
        try:
            if (self.tab == "Leg"):
                if (docType == self.docTypes[0]):
                    import unicodeConvertOdt
                    converter = unicodeConvertOdt.unicodeConvertOdt()
                    converter.convertOdtFile(inputFile, outputFile, font, fontSize)
                elif (docType == self.docTypes[2]):
                    import unicodeConvertHTML
                    unicodeConvertHTML.convertHTMLFile(inputFile, outputFile, font)
                else:
                    import unicodeConvertText
                    unicodeConvertText.convertTxtFile(inputFile, outputFile, font, encoding)
                
            else:
                if (docType == self.docTypes[0]):
                    import legacyConvertOdt
                    converter = legacyConvertOdt.legacyConvertOdt()
                    converter.convertOdtFile(inputFile, outputFile, font, fontSize)
                    
                elif (docType == self.docTypes[2]):
                    import legacyConvertHTML
                    legacyConvertHTML.convertHTML(inputFile, outputFile, font)
                else:
                    import legacyConvertText
                    legacyConvertText.convertTxtFile(inputFile, outputFile, font)
        except Exception, e:
            QtGui.QMessageBox.critical(self, self.tr("Error"), self.tr(str(e)))
            #print e
        else:
            QtGui.QMessageBox.information(self, self.tr("Information"), 
                    "Conversion successful!",
                    QtGui.QMessageBox.Yes | QtGui.QMessageBox.Default)

                
def main():
    # set the path for QT in order to find the icons
    QtCore.QDir.setCurrent(os.path.join(sys.path[0], "./images"))
    app = QtGui.QApplication(sys.argv)
    convert = Kconvert()
    convert.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
