			 khmerConverter
Copyright (c) 2006 by The WordForge Foundation (All Rights Reserved)
			www.khmeros.info

Version:	1.4	Date:	1 June 2007

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
If the result of converted odt file (OpenOffice.org Writer) is not properly, there might be problems of complex formatting which break khmer clusters.
You might have to follow these steps to solve the problem:
  1. Select the section where is not correct, then choose default formatting: (a) "right clicking" or (b) "format menu" then "default formatting"
  2. Change the selection to your desire font, for instance "Limon S1"
  3. Save and try to convert again.

IMPORTANT CHANGES:
=================

1. Added more KhmerOS fonts: KhmerOScontent.ttf, KhmerOSmuollight.ttf, KhmerOSmuolpali.ttf, KhmerOSsiemreap.ttf, 
2. Fixed the bug that when we type in the disired size in spinsize box then click on convert immediately, the size didn't change.
