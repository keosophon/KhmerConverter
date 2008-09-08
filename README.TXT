khmerConverter
Copyright (c) 2006 by Khmer Software Initiative , www.khmeros.info

Version:	1.5.1	Date:	20 August 2008

Developed by:	
	Keo Sophon (keosophon@khmeros.info)
	San Titvirak (titvirak@khmeros.info)
	Hok Kakada (hokkakada@khmeros.info)
	Seth Chanratha (sethchanratha@khmeros.info)

# This program creates a Plain Text, OpenOffice.org Writer (odt), or HTML file
# in Khmer Unicode/Legacy format from Legacy/Unicode input file respectively.
# Currently it supports legacy font types: ABC, ABC-ZWSP, Baidok, Fk, Kaoh Kong, Khek, Limon, Truth and a rasmei kampuchea...

USAGE:
======
On Windows Platform:
================
    khmerconverter.exe inputFile [outputFile] [OPTION]
        inputFile  ->  converted-inputFile
or:
    khmerconverter.exe [OPTION]
or:
    khmerconverter.exe

On Linux and all other Platforms:
======================
    python khmerconverter.py inputFile [outputFile] [OPTION]
        inputFile  ->  converted-inputFile
or:
    python khmerconverter.py or + [OPTION]

or the easy way to run KhmerConverter on Linux Please right click on desktop then Choose Create New -> Link to Application...
	 After that a dialog will pop up then choose Application tab, to fill in the same of example the following:
	 - Command:	python khmerconverter.py 
	 - Work path:	/home/ratha/Desktop/khmerconverter

If you are install from openSuSE Package, you can start KhmerConverter easy following:

For GNOME user
--------------
Goto Applications -> Accessories -> Khmer Converter

For KDE user
------------
Goto KMenu -> Utility -> Khmer Converter
 
Requirements:
	- Python-Qt4 (for GUI mode)

Running it without any option brings up the graphical user interface.

OPTION:
=======
--version	show program's version number and exit
  -h, --help	show this help message and exit
  -l, --list		list all supported fonts
  -c, --codec	list all supported codecs for text files
  -o, --oldfont	convert from unicode to old fonts (legacy)
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
===================
1. Supported one more legacy font: Rakmei Kampuchea, Kaoh Kong 
2. Changed interface to more friendly and easy to used GUI, using QT

To see any changes in each version, please read CHANGELOG.TXT file.
