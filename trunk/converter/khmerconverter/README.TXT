				 khmerConverter
	Copyright (c) 2006 by The WordForge Foundation (All Rights Reserved)
				www.khmeros.info

Version:	1.3	Date:	30 January 2007

Developed by:
	Hok Kakada (hokkakada@khmeros.info)
	Keo Sophon (keosophon@khmeros.info)
	San Titvirak (titvirak@khmeros.info)
	Seth Chanratha (sethchanratha@khmeros.info)

# This program creates a Plain Text, OpenOffice.org Writer (odt), or HTML file
# in Khmer Unicode/Legacy format from Legacy/Unicode input file respectively.
# Currently it supports legacy font types: ABC, ABC-ZWSP, Baidok, Fk, Khek, Limon, Truth

USAGE:
======

On Windows Platform:
====================
    khmerconverter.exe inputFile [outputFile] [OPTION]
        inputFile  -->  converted-inputFile
or:
    khmerconverter.exe [OPTION]
or:
    khmerconverter.exe


On Linux and all other Platforms:
=================================
    python khmerconverter.py inputFile [outputFile] [OPTION]
        inputFile  -->  converted-inputFile
or:
    python khmerconverter.py [OPTION]
or:
    python khmerconverter.py


Requirements:
	- Tix installed (for GUI mode)



Running it without any option brings up the graphical user interface.


OPTION:
=======


--version                show program's version number and exit
  -h, --help             show this help message and exit
  -l, --list             list all supported fonts
  -c, --codec            list all supported codecs for text files
  -o, --oldfont          convert from unicode to old fonts (legacy)
  -e codec, --encoding=codec
                         codec for the input file, default is 'cp1252'
  -f fontname, --font=fontname
                         fontname for output encoding, default is 'abc-zwsp'
  -s value, --size=value
                         force the program to use specific size for khmer font
  -t, --time
                         print the needed time for the conversion
                         
IMPORTANT NOTE:
In OpenOffice.org Writer, if you are not able to convert that odt file,  for example the result is still in the same font or the rendering of the converted file is not correct. you can try by:
 1. Select the section where is not correct, then choose default formatting. There are two ways: (a). right clicking. (b). format menu - default formatting
  2. Change the selection to your desire font, for instance limons1
  3. Save and try to convert again.
