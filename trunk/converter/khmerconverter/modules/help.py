# Khmer converter
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
# This module create a class for displaying help text
from Tix import *
import sys
class HelpText:

    def __init__(self, parent):
        self.root = Toplevel(parent)
        self.root.title('Help')
        if sys.platform[:6] in "windows":
            self.root.wm_iconbitmap("converter.ico")
        self.help = ScrolledText (self.root, scrollbar = 'y')
        self.help.pack(fill = BOTH, expand = 1)
        self.help.text['font'] = 'serif 12'
        self.help.subwidget_list['text'].insert(END, """Khmer Converter

Version: 1.3
Date: 30 January 2007
Copyright (c) 2006 by The WordForge Foundation (All Rights Reserved)

This program converts plain text, OpenOffice.org Writer (odt) or HTML File from 
legacy to unicode format or vice versa. The currently supported legacy fonts 
are ABC, ABC-ZWSP, Baidok, FK, Khek, Limon, and Truth. It is supported to run on 
Linux and Windows platform. But it should work on any platform that runs
Python as well.\n\n\n""")

        self.help.subwidget_list['text'].insert(END, """USAGE:

1. Choose Conversion direction:
    * Legacy to Unicode: convert old Khmer font file (ABC, Limon,...) to 
                         Khmer Unicode file
    * Unicode to Legacy: convert Khmer unicode file to 
                         old Khmer font file (ABC, Limon, ...)

2. Choose Input:
    * File: file to convert   
    * Document Type:
        - Plain text: just the normal text file.
        - OpenOffice.org Writer: for OpenOffice Writer file with extension .odt
        - HTML: for web page file.
    * Font: old fonts of the input file
    * Encoding:
        - Plain Text (cp1252): for file with Khmer legacy character.
        - Plain Text (latin-1/iso-8859-1): for file with Khmer legacy character.
        - UTF-8 : for file with unicode character.

3. Choose Ouput:
    * File: result file after conversion.    
    * Font (for OpenOffice.Org writer): font for output file.
    * Override size (OpenOffice.Org writer): force converter to use specific 
                     size for output file, leave unchecked to use font size 
                     according to input file.

4. Click "Convert" button
    * A message box will confirm you whether it is successful or not.\n\n\n""")        
    

    
        self.help.subwidget_list['text'].insert(END, """AUTHORS
            
    - Hok Kakada (hokkakada@khmeros.info)\n
    - Keo Sophon (keosophon@khmeros.info)\n
    - San Titvirak (titvirak@khmeros.info)\n
    - Seth Chanratha (sethchanratha@khmeros.info)\n\n\n""")
        self.help.subwidget_list['text'].insert(END, """LICENSE
        
This program is free software; you can redistribute it and/or modify it under 
the terms of the GNU Lesser General Public License as published by the Free 
Software Foundation; either version 2.1 of the License, or (at your option) 
any later version.
        
Please see more details about license\nhttp://www.gnu.org/licenses/lgpl.html\n\n""")

        self.help.text['state'] = 'disabled'
