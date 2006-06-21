#Khmer converter
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
# This module create a graphical user interface using basically on Tix module

from Tix import *
from mimetypes import MimeTypes
import tkMessageBox
import FontDataXML
import os
import tkFont

# constants
TOUNICODE = 'unicode'
TOLEGACY = 'legacy'
TYPETEXT = 'Plain Text'
TYPEODT = 'OpenOffice.org Writer (*.odt)'
TYPEHTML = 'Web Page, HTML'
CODEISO = 'Plain Text (latin-1/iso-8859-1)'
CODEUTF = 'Unicode (utf-8)'
DEFAULTFONTSIZE = 11

# default value
def setDefault():
    directionVar.set(TOUNICODE)
    cmbDocType.pick(0)
    cmbEncoding.pick(0)
    cmbFontInput.pick(INDEXABCZWSP)
    cmbFontOutput.pick(INDEXKHMEROS)
    
    docTypeVar.set(TYPETEXT)
    fntInput.entry.delete(0, END)
    outputFileVar.set('')
    spnSize['state'] = NORMAL
    fontSizeVar.set(DEFAULTFONTSIZE)
    spnSize['state'] = DISABLED
    chkSize.deselect()
    evUnicodeClick()
    checkStatus()
    
def checkConvertible():
    if (inputFileVar.get() and outputFileVar.get()):
        btnConvert['state'] = NORMAL
    else:
        btnConvert['state'] = DISABLED
       
def checkStatus():
    cmbEncoding['state'] = DISABLED
    cmbEncoding.set_silent(' ')
    
    if (directionVar.get() == TOUNICODE):
        cmbFontInput['state'] = NORMAL
        cmbFontInput.pick(INDEXABCZWSP)
        if (docTypeVar.get() == TYPEODT):
            cmbFontOutput['state'] = NORMAL
            cmbFontOutput.pick(INDEXKHMEROS)
            cmbFontInput['state'] = DISABLED
            cmbFontInput.set_silent(' ')
            chkSize['state'] = NORMAL
        elif (docTypeVar.get() == TYPETEXT):
            cmbEncoding['state'] = NORMAL
            cmbEncoding.pick(0)
            cmbFontOutput['state'] = DISABLED
            cmbFontOutput.set_silent(' ')
            chkSize['state'] = DISABLED
            spnSize['state'] = DISABLED
            chkSize.deselect()
        elif (docTypeVar.get() == TYPEHTML):
            cmbFontOutput['state'] = DISABLED
            cmbFontOutput.set_silent(' ')
            chkSize['state'] = DISABLED
            spnSize['state'] = DISABLED
            chkSize.deselect()

    else:
        cmbFontInput['state'] = DISABLED
        cmbFontInput.set_silent(' ')
        cmbFontOutput['state'] = NORMAL
        if (docTypeVar.get() == TYPEODT):
            chkSize['state'] = NORMAL
        else:            
            chkSize['state'] = DISABLED
            spnSize['state'] = DISABLED
            chkSize.deselect()

# event handler
def evResetClick():
    setDefault()

def evSetInput(val):
    mimeType = mt.guess_type(inputFileVar.get())[0]
    if (mimeType == 'application/vnd.oasis.opendocument.text'):
        docTypeVar.set(TYPEODT)
    elif (mimeType == 'text/html' or mimeType == 'text/xml'):
        docTypeVar.set(TYPEHTML)
    elif (mimeType == None):
        # if mimeType failed to give apropriet value, use file
        # extension instead.
        filename = inputFileVar.get().lower()
        if filename.endswith('.odt'):
            docTypeVar.set(TYPEODT)
        elif filename.endswith('.htm') or filename.endswith('.html'):
            docTypeVar.set(TYPEHTML)
        else:
            docTypeVar.set(TYPETEXT)
    else:
        docTypeVar.set(TYPETEXT)
    cmbDocType.set_silent(docTypeVar.get())

#  set outputFile according to inputFile
    (path, filename) = os.path.split(inputFileVar.get())
    outputFileVar.set(os.path.join(path, 'converted-' + filename))
    checkStatus()
    checkConvertible()

def evSetOutput(val):
    checkConvertible()

def evChkSize():
    if chkSizeVar.get():
        spnSize['state'] = NORMAL
    else:
        spnSize['state'] = DISABLED   

def evDocumentTypeClick(val):
    if (val):
        checkStatus()

def evUnicodeClick():
    cmbFontOutput.slistbox.listbox.delete(0,END)
    for font in unicodeFontList:
        cmbFontOutput.insert(END, font)
    cmbFontOutput.pick(INDEXKHMEROS)
    checkStatus()   

def evLegacyClick():
    cmbFontOutput.slistbox.listbox.delete(0,END)
    for font in legacyFontList:
        cmbFontOutput.insert(END, font)
    cmbFontOutput.pick(INDEXABCZWSP)
    checkStatus()

def evHelp():
    # create the top level window/frame    
    import help    
    helptext = help.HelpText(top)
    btnHelp['state'] = DISABLED
    top.wait_window(helptext.root)
    # use try because the widget might not exist anymore
    try:
        btnHelp['state'] = NORMAL
    except:
        pass
        
def evQuit():
    top.destroy()
    
def evConvert():
    btnConvert.focus_set()
    encoding = encodingVar.get()
    if (encoding == CODEISO):
        encoding = 'iso-8859-1'
    elif (encoding == CODEUTF):
        encoding = 'utf-8'
    else:
        encoding = 'cp1252'
       
    # output font is priority
    if (cmbFontOutput['state'] == NORMAL):
        font = fontOutVar.get().lstrip()
    else:
        font = fontInVar.get().lstrip()

    # set font size to zero if it is disabled
    if (spnSize['state'] == DISABLED):
        fontSize = None
    else:
        fontSize = fontSizeVar.get()
    
    direction = directionVar.get()
    inputFile = inputFileVar.get()
    docType = docTypeVar.get()
    outputFile = outputFileVar.get()

    # check if output file already exist
    if (os.path.exists(outputFile)):
        confirm = tkMessageBox.askquestion('Warning', 'The output file does already exist!\n\nDo you want to overwrite?')
        if (confirm == 'no'):
            return

    try:
        if (direction == TOUNICODE):
            if (docType == TYPEODT):
                import unicodeConvertOdt
                unicodeConvertOdt.convertOdtFile(inputFile, outputFile, font, fontSize)
            elif (docType == TYPEHTML):
                import unicodeConvertHTML
                unicodeConvertHTML.convertHTMLFile(inputFile, outputFile, font)
            else:
                import unicodeConvertText
                unicodeConvertText.convertTxtFile(inputFile, outputFile, font, encoding)
                
        else:
            if (docType == TYPEODT):
                import legacyConvertOdt
                legacyConvertOdt.convertOdtFile(inputFile, outputFile, font, fontSize)
                
            elif (docType == TYPEHTML):
                import legacyConvertHTML
                legacyConvertHTML.convertHTML(inputFile, outputFile, font)
            else:
                import legacyConvertText
                legacyConvertText.convertTxtFile(inputFile, outputFile, font)
    except Exception, e:
        tkMessageBox.showerror('Error', e)
    else:
        tkMessageBox.showinfo('Information', 'Conversion successful!')
# instance of mime type
mt = MimeTypes()

# create the top level window/frame
top = Tk()
top.wm_title('Khmer Converter 1.0')
top.protocol("WM_DELETE_WINDOW", top.destroy)
top.geometry("500x550+150+150")
top.minsize(450, 480)
frmTop = Frame(top)

FONTSIZE = tkFont.Font(family="serif", size=DEFAULTFONTSIZE, weight="normal")

#default color
bgcol = "light blue"

# create frame
frmDirection = LabelFrame(frmTop, border=1, borderwidth=1, relief=GROOVE, label ='Conversion direction', labelside=TOP, bg=bgcol)
frmDirection.label.configure(font = FONTSIZE)
frmInput = LabelFrame(frmTop, border=1, borderwidth=1, relief=GROOVE, label='Input', labelside=TOP, bg=bgcol)
frmInput.label.configure(font = FONTSIZE)
frmOutput = LabelFrame(frmTop, border=1, borderwidth=1, relief=GROOVE, label='Output', labelside=TOP, bg=bgcol)
frmOutput.label.configure(font = FONTSIZE)
frmButton = Frame(frmTop, border=1, borderwidth=1)

# create some widgets inside

# widgets for direction
directionVar = StringVar()
radUnicode = Radiobutton(frmDirection.frame, text="Legacy to Unicode", font=FONTSIZE, command=evUnicodeClick, value=TOUNICODE, variable=directionVar)
radLegacy = Radiobutton(frmDirection.frame, text="Unicode to Legacy", font=FONTSIZE, command=evLegacyClick, value=TOLEGACY, variable=directionVar)

# widgets for input
inputFileVar = StringVar()
frmInputSub = Frame(frmInput.frame)
lblInput = Label(frmInputSub, text='File:', font=FONTSIZE)
fntInput = FileEntry(frmInputSub, dialogtype = 'tk_getOpenFile', width = 50, command=evSetInput, variable=inputFileVar)
fntInput.entry.configure(font=FONTSIZE)
docTypeVar = StringVar()
cmbDocType = ComboBox(frmInput.frame, label="Document Type:", dropdown=1, editable=1, variable=docTypeVar, options='listbox.height 3', command=evDocumentTypeClick)
cmbDocType.entry.configure(width=30, font=FONTSIZE)
cmbDocType.label.configure(font = FONTSIZE)
fontInVar = StringVar()
cmbFontInput = ComboBox(frmInput.frame, label="Font:", dropdown=1, editable=1, variable=fontInVar)
cmbFontInput.entry.configure(width=30, font = FONTSIZE)
cmbFontInput.label.configure(font = FONTSIZE)
encodingVar = StringVar()
cmbEncoding = ComboBox(frmInput.frame, label = "Encoding:", dropdown=1, editable=1, variable=encodingVar, options='listbox.height 3' )
cmbEncoding.entry.configure(width=30, font=FONTSIZE)
cmbEncoding.label.configure(font=FONTSIZE)
# widgets for output
outputFileVar = StringVar()
frmOutputSub = Frame(frmOutput.frame)
lblOutput = Label(frmOutputSub, text='File:', font=FONTSIZE)
fntOutput = FileEntry(frmOutputSub, dialogtype='tk_getSaveFile', command=evSetOutput, variable=outputFileVar)
fntOutput.entry.configure(font=FONTSIZE)
fontOutVar = StringVar()
cmbFontOutput = ComboBox(frmOutput.frame, label="Font:", dropdown = 1, editable=1, variable=fontOutVar)
cmbFontOutput.entry.configure(width=30, font=FONTSIZE)
cmbFontOutput.label.configure(font=FONTSIZE)
frmSize = Frame(frmOutput.frame)
chkSizeVar = IntVar()
chkSize = Checkbutton(frmSize, text='Override size', variable=chkSizeVar, command=evChkSize, font=FONTSIZE)
fontSizeVar = IntVar()
spnSize = Control(frmSize, label='Size:', min=1, max=100, variable=fontSizeVar, value=DEFAULTFONTSIZE)
spnSize.label.configure(font=FONTSIZE)
spnSize.entry.configure(font=FONTSIZE, justify=RIGHT)

#widgets for buttons
btnConvert = Button(frmButton, text='Convert', command=evConvert, width=7, font = FONTSIZE)
btnReset = Button(frmButton, text='Reset', command=evResetClick, width=7, font = FONTSIZE)
btnHelp = Button(frmButton, text='Help', command=evHelp, width=7, font = FONTSIZE)
btnQuit = Button(frmButton, text='Quit', command=evQuit, width=7, font = FONTSIZE)

# pack the widgets
frmTop.pack(fill=BOTH, expand=1)
frmDirection.pack(fill=BOTH, expand=1, padx=10, pady=10)
frmInput.pack(fill=BOTH, expand=1, padx=10)
frmOutput.pack(fill=BOTH, expand=1, padx=10, pady=10)
frmButton.pack(fill=BOTH, expand=1, padx=5)
# direction
radUnicode.pack(anchor=W, padx=10)
radLegacy.pack(anchor=W, padx=10)
# input
frmInputSub.pack(anchor=W, fill=X, expand=1, padx=10, pady=5)
lblInput.pack(side=LEFT, anchor=W)
fntInput.pack(side=LEFT, anchor=W, fill=X, expand=1)
cmbDocType.pack(anchor=E, padx=10, pady=5)
cmbFontInput.pack(anchor=E, padx=10, pady=5)
cmbEncoding.pack(anchor=E, padx=10, pady=5)
# output
frmOutputSub.pack(anchor=W, fill=X, expand=1, padx=10, pady=5)
lblOutput.pack(side=LEFT, anchor=W)
fntOutput.pack(side=LEFT, anchor=W, fill=X, expand=1)
cmbFontOutput.pack(anchor=E, padx=10, pady=5)
frmSize.pack(side=RIGHT, padx=10, pady=5)
chkSize.pack(side=LEFT, anchor=E, padx=10, pady=5)
spnSize.pack(side=LEFT, anchor=E)
# buttons
btnConvert.pack(side=LEFT, padx=5, anchor=NW)
btnReset.pack(side=LEFT, padx=5, anchor=NW)
btnHelp.pack(side=LEFT, padx=5, anchor=NW)
btnQuit.pack(side=LEFT, padx=5, anchor=NW)

# set value for all combo box
fd = FontDataXML.FontData()
legacyFontList = []
for font in fd.listFontTypes():
    legacyFontList.append(font)
    for fontName in fd.listFontNamesForType(font):
        legacyFontList.append("  " + fontName)

unicodeFontList = ['Khmer OS', 'Khmer OS Bokor', 'Khmer OS Fasthand', 'Khmer OS Freehand','Khmer OS Metal Chrieng', 'Khmer OS Moul', 'Khmer OS System']
encodingList = fd.listEncodingTypes()
documentList = [TYPETEXT, TYPEODT, TYPEHTML]

for font in legacyFontList:
    cmbFontInput.insert(END, font)
for font in unicodeFontList:
    cmbFontOutput.insert(END, font)
for encoding in encodingList:
    cmbEncoding.insert(END, encoding)
for documenttype in documentList:
    cmbDocType.insert(END, documenttype)

# get index for abc-zwsp
INDEXABCZWSP = 0
for i in range(len(legacyFontList)):
    if (legacyFontList[i] == 'abc-zwsp'):
        INDEXABCZWSP = i
        break

# get index for khmer os
INDEXKHMEROS = 0
for i in range(len(unicodeFontList)):
    if (unicodeFontList[i] == 'Khmer OS'):
        INDEXKHMEROS = i
        break

evResetClick()

# set the loop running
top.mainloop()
