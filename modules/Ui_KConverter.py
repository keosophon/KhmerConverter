# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '/home/k-da/Desktop/temp/daDesktop/svn-khmerconverter/svn/khmerconverter_new/modules/KConverter.ui'
#
# Created: Fri Nov  2 14:59:02 2007
#      by: PyQt4 UI code generator 4-snapshot-20070212
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_kconvert(object):
    def setupUi(self, kconvert):
        kconvert.setObjectName("kconvert")
        kconvert.resize(QtCore.QSize(QtCore.QRect(0,0,462,460).size()).expandedTo(kconvert.minimumSizeHint()))
        kconvert.setWindowIcon(QtGui.QIcon("../images/converter.png"))

        self.centralwidget = QtGui.QWidget(kconvert)
        self.centralwidget.setObjectName("centralwidget")

        self.gridlayout = QtGui.QGridLayout(self.centralwidget)
        self.gridlayout.setMargin(9)
        self.gridlayout.setSpacing(6)
        self.gridlayout.setObjectName("gridlayout")

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        self.tab1 = QtGui.QWidget()
        self.tab1.setObjectName("tab1")

        self.gridlayout1 = QtGui.QGridLayout(self.tab1)
        self.gridlayout1.setMargin(9)
        self.gridlayout1.setSpacing(6)
        self.gridlayout1.setObjectName("gridlayout1")

        self.groupBox_2 = QtGui.QGroupBox(self.tab1)
        self.groupBox_2.setObjectName("groupBox_2")

        self.gridlayout2 = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout2.setMargin(9)
        self.gridlayout2.setSpacing(6)
        self.gridlayout2.setObjectName("gridlayout2")

        self.cmbFontOutputL = QtGui.QComboBox(self.groupBox_2)
        self.cmbFontOutputL.setObjectName("cmbFontOutputL")
        self.gridlayout2.addWidget(self.cmbFontOutputL,1,1,1,4)

        self.label_10 = QtGui.QLabel(self.groupBox_2)
        self.label_10.setObjectName("label_10")
        self.gridlayout2.addWidget(self.label_10,1,0,1,1)

        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setMargin(0)
        self.hboxlayout.setSpacing(6)
        self.hboxlayout.setObjectName("hboxlayout")

        self.lineOutputL = QtGui.QLineEdit(self.groupBox_2)
        self.lineOutputL.setObjectName("lineOutputL")
        self.hboxlayout.addWidget(self.lineOutputL)

        self.btnBrowseOutL = QtGui.QPushButton(self.groupBox_2)
        self.btnBrowseOutL.setIcon(QtGui.QIcon("../images/open.png"))
        self.btnBrowseOutL.setObjectName("btnBrowseOutL")
        self.hboxlayout.addWidget(self.btnBrowseOutL)
        self.gridlayout2.addLayout(self.hboxlayout,0,1,1,4)

        self.label_9 = QtGui.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.gridlayout2.addWidget(self.label_9,0,0,1,1)

        self.chbOverrideSizeL = QtGui.QCheckBox(self.groupBox_2)
        self.chbOverrideSizeL.setEnabled(False)
        self.chbOverrideSizeL.setChecked(True)
        self.chbOverrideSizeL.setObjectName("chbOverrideSizeL")
        self.gridlayout2.addWidget(self.chbOverrideSizeL,2,1,1,1)

        self.lblSizeL = QtGui.QLabel(self.groupBox_2)
        self.lblSizeL.setEnabled(False)
        self.lblSizeL.setObjectName("lblSizeL")
        self.gridlayout2.addWidget(self.lblSizeL,2,3,1,1)

        self.spinBoxSizeL = QtGui.QSpinBox(self.groupBox_2)
        self.spinBoxSizeL.setEnabled(False)
        self.spinBoxSizeL.setObjectName("spinBoxSizeL")
        self.gridlayout2.addWidget(self.spinBoxSizeL,2,4,1,1)

        spacerItem = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout2.addItem(spacerItem,2,2,1,1)
        self.gridlayout1.addWidget(self.groupBox_2,1,0,1,1)

        spacerItem1 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout1.addItem(spacerItem1,2,0,1,1)

        self.groupBox = QtGui.QGroupBox(self.tab1)
        self.groupBox.setObjectName("groupBox")

        self.gridlayout3 = QtGui.QGridLayout(self.groupBox)
        self.gridlayout3.setMargin(9)
        self.gridlayout3.setSpacing(6)
        self.gridlayout3.setObjectName("gridlayout3")

        self.lineInputL = QtGui.QLineEdit(self.groupBox)
        self.lineInputL.setObjectName("lineInputL")
        self.gridlayout3.addWidget(self.lineInputL,0,1,1,1)

        self.cmbDocTypeL = QtGui.QComboBox(self.groupBox)
        self.cmbDocTypeL.setObjectName("cmbDocTypeL")
        self.gridlayout3.addWidget(self.cmbDocTypeL,1,1,1,2)

        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridlayout3.addWidget(self.label_2,1,0,1,1)

        self.label = QtGui.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridlayout3.addWidget(self.label,0,0,1,1)

        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridlayout3.addWidget(self.label_3,2,0,1,1)

        self.label_4 = QtGui.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.gridlayout3.addWidget(self.label_4,3,0,1,1)

        self.btnBrowseInL = QtGui.QPushButton(self.groupBox)
        self.btnBrowseInL.setIcon(QtGui.QIcon("../images/open.png"))
        self.btnBrowseInL.setObjectName("btnBrowseInL")
        self.gridlayout3.addWidget(self.btnBrowseInL,0,2,1,1)

        self.cmbEncodingL = QtGui.QComboBox(self.groupBox)
        self.cmbEncodingL.setObjectName("cmbEncodingL")
        self.gridlayout3.addWidget(self.cmbEncodingL,3,1,1,2)

        self.cmbFontInputL = QtGui.QComboBox(self.groupBox)
        self.cmbFontInputL.setObjectName("cmbFontInputL")
        self.gridlayout3.addWidget(self.cmbFontInputL,2,1,1,2)
        self.gridlayout1.addWidget(self.groupBox,0,0,1,1)
        self.tabWidget.addTab(self.tab1,"")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.gridlayout4 = QtGui.QGridLayout(self.tab)
        self.gridlayout4.setMargin(9)
        self.gridlayout4.setSpacing(6)
        self.gridlayout4.setObjectName("gridlayout4")

        self.groupBox_4 = QtGui.QGroupBox(self.tab)
        self.groupBox_4.setObjectName("groupBox_4")

        self.gridlayout5 = QtGui.QGridLayout(self.groupBox_4)
        self.gridlayout5.setMargin(9)
        self.gridlayout5.setSpacing(6)
        self.gridlayout5.setObjectName("gridlayout5")

        self.cmbFontOutputU = QtGui.QComboBox(self.groupBox_4)
        self.cmbFontOutputU.setObjectName("cmbFontOutputU")
        self.gridlayout5.addWidget(self.cmbFontOutputU,1,1,1,4)

        self.label_14 = QtGui.QLabel(self.groupBox_4)
        self.label_14.setObjectName("label_14")
        self.gridlayout5.addWidget(self.label_14,0,0,1,1)

        self.hboxlayout1 = QtGui.QHBoxLayout()
        self.hboxlayout1.setMargin(0)
        self.hboxlayout1.setSpacing(6)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.lineOutputU = QtGui.QLineEdit(self.groupBox_4)
        self.lineOutputU.setObjectName("lineOutputU")
        self.hboxlayout1.addWidget(self.lineOutputU)

        self.btnBrowseOutU = QtGui.QPushButton(self.groupBox_4)
        self.btnBrowseOutU.setIcon(QtGui.QIcon("../images/open.png"))
        self.btnBrowseOutU.setObjectName("btnBrowseOutU")
        self.hboxlayout1.addWidget(self.btnBrowseOutU)
        self.gridlayout5.addLayout(self.hboxlayout1,0,1,1,4)

        self.label_15 = QtGui.QLabel(self.groupBox_4)
        self.label_15.setObjectName("label_15")
        self.gridlayout5.addWidget(self.label_15,1,0,1,1)

        self.chbOverrideSizeU = QtGui.QCheckBox(self.groupBox_4)
        self.chbOverrideSizeU.setEnabled(False)
        self.chbOverrideSizeU.setObjectName("chbOverrideSizeU")
        self.gridlayout5.addWidget(self.chbOverrideSizeU,2,1,1,1)

        spacerItem2 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout5.addItem(spacerItem2,2,2,1,1)

        self.lblSizeU = QtGui.QLabel(self.groupBox_4)
        self.lblSizeU.setEnabled(False)
        self.lblSizeU.setObjectName("lblSizeU")
        self.gridlayout5.addWidget(self.lblSizeU,2,3,1,1)

        self.spinBoxSizeU = QtGui.QSpinBox(self.groupBox_4)
        self.spinBoxSizeU.setEnabled(False)
        self.spinBoxSizeU.setObjectName("spinBoxSizeU")
        self.gridlayout5.addWidget(self.spinBoxSizeU,2,4,1,1)
        self.gridlayout4.addWidget(self.groupBox_4,1,0,1,1)

        self.groupBox_3 = QtGui.QGroupBox(self.tab)
        self.groupBox_3.setObjectName("groupBox_3")

        self.gridlayout6 = QtGui.QGridLayout(self.groupBox_3)
        self.gridlayout6.setMargin(9)
        self.gridlayout6.setSpacing(6)
        self.gridlayout6.setObjectName("gridlayout6")

        self.label_6 = QtGui.QLabel(self.groupBox_3)
        self.label_6.setObjectName("label_6")
        self.gridlayout6.addWidget(self.label_6,0,0,1,1)

        self.btnBrowseInU = QtGui.QPushButton(self.groupBox_3)
        self.btnBrowseInU.setIcon(QtGui.QIcon("../images/open.png"))
        self.btnBrowseInU.setObjectName("btnBrowseInU")
        self.gridlayout6.addWidget(self.btnBrowseInU,0,2,1,1)

        self.label_5 = QtGui.QLabel(self.groupBox_3)
        self.label_5.setObjectName("label_5")
        self.gridlayout6.addWidget(self.label_5,1,0,1,1)

        self.cmbDocTypeU = QtGui.QComboBox(self.groupBox_3)
        self.cmbDocTypeU.setObjectName("cmbDocTypeU")
        self.gridlayout6.addWidget(self.cmbDocTypeU,1,1,1,2)

        self.lineInputU = QtGui.QLineEdit(self.groupBox_3)
        self.lineInputU.setObjectName("lineInputU")
        self.gridlayout6.addWidget(self.lineInputU,0,1,1,1)
        self.gridlayout4.addWidget(self.groupBox_3,0,0,1,1)

        spacerItem3 = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.gridlayout4.addItem(spacerItem3,2,0,1,1)
        self.tabWidget.addTab(self.tab,"")
        self.gridlayout.addWidget(self.tabWidget,0,0,1,3)

        self.btnReset = QtGui.QPushButton(self.centralwidget)
        self.btnReset.setObjectName("btnReset")
        self.gridlayout.addWidget(self.btnReset,1,1,1,1)

        spacerItem4 = QtGui.QSpacerItem(40,20,QtGui.QSizePolicy.Expanding,QtGui.QSizePolicy.Minimum)
        self.gridlayout.addItem(spacerItem4,1,2,1,1)

        self.btnConvert = QtGui.QPushButton(self.centralwidget)
        self.btnConvert.setObjectName("btnConvert")
        self.gridlayout.addWidget(self.btnConvert,1,0,1,1)
        kconvert.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(kconvert)
        self.menubar.setGeometry(QtCore.QRect(0,0,462,29))
        self.menubar.setObjectName("menubar")

        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName("menu_Help")

        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        kconvert.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(kconvert)
        self.statusbar.setObjectName("statusbar")
        kconvert.setStatusBar(self.statusbar)

        self.actionQuit = QtGui.QAction(kconvert)
        self.actionQuit.setIcon(QtGui.QIcon("../images/exit.png"))
        self.actionQuit.setObjectName("actionQuit")

        self.actionLegacy_to_Unicode = QtGui.QAction(kconvert)
        self.actionLegacy_to_Unicode.setObjectName("actionLegacy_to_Unicode")

        self.actionUnicode_to_Legacy = QtGui.QAction(kconvert)
        self.actionUnicode_to_Legacy.setObjectName("actionUnicode_to_Legacy")

        self.actionAboutKConverter = QtGui.QAction(kconvert)
        self.actionAboutKConverter.setObjectName("actionAboutKConverter")

        self.actionAboutQt = QtGui.QAction(kconvert)
        self.actionAboutQt.setObjectName("actionAboutQt")
        self.menu_Help.addAction(self.actionAboutKConverter)
        self.menu_Help.addAction(self.actionAboutQt)
        self.menu_File.addAction(self.actionQuit)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())

        self.retranslateUi(kconvert)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(kconvert)
        kconvert.setTabOrder(self.tabWidget,self.lineInputL)
        kconvert.setTabOrder(self.lineInputL,self.btnBrowseInU)
        kconvert.setTabOrder(self.btnBrowseInU,self.cmbDocTypeL)
        kconvert.setTabOrder(self.cmbDocTypeL,self.cmbFontInputL)
        kconvert.setTabOrder(self.cmbFontInputL,self.cmbEncodingL)
        kconvert.setTabOrder(self.cmbEncodingL,self.btnConvert)
        kconvert.setTabOrder(self.btnConvert,self.btnReset)

    def retranslateUi(self, kconvert):
        kconvert.setWindowTitle(QtGui.QApplication.translate("kconvert", "Khmer Converter", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("kconvert", "Output File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setText(QtGui.QApplication.translate("kconvert", "Font:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("kconvert", "Filename:", None, QtGui.QApplication.UnicodeUTF8))
        self.chbOverrideSizeL.setText(QtGui.QApplication.translate("kconvert", "Override size", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSizeL.setText(QtGui.QApplication.translate("kconvert", "Size:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("kconvert", "Input File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("kconvert", "Document type:", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("kconvert", "Filename:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("kconvert", "Font:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setText(QtGui.QApplication.translate("kconvert", "Encoding:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab1), QtGui.QApplication.translate("kconvert", "Legacy to Unicode", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("kconvert", "Output File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_14.setText(QtGui.QApplication.translate("kconvert", "Filename:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_15.setText(QtGui.QApplication.translate("kconvert", "Font:", None, QtGui.QApplication.UnicodeUTF8))
        self.chbOverrideSizeU.setText(QtGui.QApplication.translate("kconvert", "Override size", None, QtGui.QApplication.UnicodeUTF8))
        self.lblSizeU.setText(QtGui.QApplication.translate("kconvert", "Size:", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("kconvert", "Input File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("kconvert", "Filename:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setText(QtGui.QApplication.translate("kconvert", "Document type:", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("kconvert", "Unicode to Legacy", None, QtGui.QApplication.UnicodeUTF8))
        self.btnReset.setText(QtGui.QApplication.translate("kconvert", "&Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.btnConvert.setText(QtGui.QApplication.translate("kconvert", "&Convert", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("kconvert", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("kconvert", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setText(QtGui.QApplication.translate("kconvert", "&Quit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionQuit.setShortcut(QtGui.QApplication.translate("kconvert", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLegacy_to_Unicode.setText(QtGui.QApplication.translate("kconvert", "Legacy to Unicode", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLegacy_to_Unicode.setShortcut(QtGui.QApplication.translate("kconvert", "Ctrl+L", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUnicode_to_Legacy.setText(QtGui.QApplication.translate("kconvert", "Unicode to Legacy", None, QtGui.QApplication.UnicodeUTF8))
        self.actionUnicode_to_Legacy.setShortcut(QtGui.QApplication.translate("kconvert", "Ctrl+U", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAboutKConverter.setText(QtGui.QApplication.translate("kconvert", "About Khmer Unicode", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAboutQt.setText(QtGui.QApplication.translate("kconvert", "About Qt", None, QtGui.QApplication.UnicodeUTF8))



if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    kconvert = QtGui.QMainWindow()
    ui = Ui_kconvert()
    ui.setupUi(kconvert)
    kconvert.show()
    sys.exit(app.exec_())
