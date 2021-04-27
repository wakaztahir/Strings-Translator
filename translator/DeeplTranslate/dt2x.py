#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This python skript parses strings from a text file into a given
# XML file. 

# run via 

# PYTHONIOENCODING=utf8 python3.5 dt2x.py strings.xml strings.txt "::"

# where firstly the environment variable PYTHONENCODING is set,
# then python is called,
# then the name of the current file plus argument strings, 
# where the first argument is the xml input file and
# the second argument is the text file containing the strings and
# the third argument is the unique delimiter that should be used.
#
# The new XML file has "_CP" appended to the base file name. 

### LANGUAGE CODES FOR REFERENCE

#   af          Afrikaans
#   ak          Akan
#   sq          Albanian
#   am          Amharic
#   ar          Arabic
#   hy          Armenian
#   az          Azerbaijani
#   eu          Basque
#   be          Belarusian
#   bem         Bemba
#   bn          Bengali
#   bh          Bihari
#   xx-bork     Bork, bork, bork!
#   bs          Bosnian
#   br          Breton
#   bg          Bulgarian
#   km          Cambodian
#   ca          Catalan
#   chr         Cherokee
#   ny          Chichewa
#   zh-CN       Chinese (Simplified)
#   zh-TW       Chinese (Traditional)
#   co          Corsican
#   hr          Croatian
#   cs          Czech
#   da          Danish
#   nl          Dutch
#   xx-elmer    Elmer Fudd
#   en          English
#   eo          Esperanto
#   et          Estonian
#   ee          Ewe
#   fo          Faroese
#   tl          Filipino
#   fi          Finnish
#   fr          French
#   fy          Frisian
#   gaa         Ga
#   gl          Galician
#   ka          Georgian
#   de          German
#   el          Greek
#   gn          Guarani
#   gu          Gujarati
#   xx-hacker   Hacker
#   ht          Haitian Creole
#   ha          Hausa
#   haw         Hawaiian
#   iw          Hebrew
#   hi          Hindi
#   hu          Hungarian
#   is          Icelandic
#   ig          Igbo
#   id          Indonesian
#   ia          Interlingua
#   ga          Irish
#   it          Italian
#   ja          Japanese
#   jw          Javanese
#   kn          Kannada
#   kk          Kazakh
#   rw          Kinyarwanda
#   rn          Kirundi
#   xx-klingon  Klingon
#   kg          Kongo
#   ko          Korean
#   kri         Krio (Sierra Leone)
#   ku          Kurdish
#   ckb         Kurdish (Soranî)
#   ky          Kyrgyz
#   lo          Laothian
#   la          Latin
#   lv          Latvian
#   ln          Lingala
#   lt          Lithuanian
#   loz         Lozi
#   lg          Luganda
#   ach         Luo
#   mk          Macedonian
#   mg          Malagasy
#   ms          Malay
#   ml          Malayalam
#   mt          Maltese
#   mi          Maori
#   mr          Marathi
#   mfe         Mauritian Creole
#   mo          Moldavian
#   mn          Mongolian
#   sr-ME       Montenegrin
#   ne          Nepali
#   pcm         Nigerian Pidgin
#   nso         Northern Sotho
#   no          Norwegian
#   nn          Norwegian (Nynorsk)
#   oc          Occitan
#   or          Oriya
#   om          Oromo
#   ps          Pashto
#   fa          Persian
#   xx-pirate   Pirate
#   pl          Polish
#   pt-BR       Portuguese (Brazil)
#   pt-PT       Portuguese (Portugal)
#   pa          Punjabi
#   qu          Quechua
#   ro          Romanian
#   rm          Romansh
#   nyn         Runyakitara
#   ru          Russian
#   gd          Scots Gaelic
#   sr          Serbian
#   sh          Serbo-Croatian
#   st          Sesotho
#   tn          Setswana
#   crs         Seychellois Creole
#   sn          Shona
#   sd          Sindhi
#   si          Sinhalese
#   sk          Slovak
#   sl          Slovenian
#   so          Somali
#   es          Spanish
#   es-419      Spanish (Latin American)
#   su          Sundanese
#   sw          Swahili
#   sv          Swedish
#   tg          Tajik
#   ta          Tamil
#   tt          Tatar
#   te          Telugu
#   th          Thai
#   ti          Tigrinya
#   to          Tonga
#   lua         Tshiluba
#   tum         Tumbuka
#   tr          Turkish
#   tk          Turkmen
#   tw          Twi
#   ug          Uighur
#   uk          Ukrainian
#   ur          Urdu
#   uz          Uzbek
#   vi          Vietnamese
#   cy          Welsh
#   wo          Wolof
#   xh          Xhosa
#   yi          Yiddish
#   yo          Yoruba
#   zu          Zulu


#
# MAIN PROGRAM
#

import io
import os
import sys
# import libraries
import xml.etree.ElementTree as ET

# read argument vector
XMLINFILE = sys.argv[1]
STRINGINFILE = sys.argv[2]
DELIM = sys.argv[3]

# create outfile name by appending CP (copy-paste) to the infile name
name, ext = os.path.splitext(XMLINFILE)
OUTFILE = "{name}_{CP}{ext}".format(name=name, CP="CP", ext=ext)

# open XML file and string text file
tree = ET.parse(XMLINFILE)  # read_xml_file(XMLINFILE)
root = tree.getroot()
file = io.open(STRINGINFILE, 'r', encoding="utf-8")

# read all lines from string text file and convert to utf8 string
# then close string text file
translations = file.readlines()
alltrans = "".join(translations)
file.close()

counter = 0
for i in range(len(root)):
    #	replace each translatable string by corresponding string from text file
    #   descend into each string array
    isTranslatable = root[i].get('translatable')
    if (root[i].tag == 'string') & (isTranslatable != 'false'):
        ste = root[i].text
        print(str(counter) + DELIM + ste)
        counter = counter + 1
        #       remove trailing numbers and line breaks
        value = alltrans.split(DELIM, counter)[-1].split(DELIM, 1)[0].rstrip('1234567890\n').lstrip(" ")
        root[i].text = value
        #       echo string replacement
        print("-->" + value)
    else:
        if (root[i].tag == 'string-array') & (isTranslatable != 'false'):
            for j in range(len(root[i])):
                if (root[i][j].tag == 'item'):
                    isTranslatable = root[i][j].get('translatable')
                    if (isTranslatable != 'false'):
                        counter = counter + 1
                        #                       remove trailing numbers and line breaks
                        value = alltrans.split(DELIM, counter)[-1].split(DELIM, 1)[0].rstrip('1234567890\n').lstrip(" ")
                        ste = root[i][j].text
                        print(str(counter) + DELIM + ste)
                        root[i][j].text = value
                        #                       echo string replacement
                        print("-->" + value)

# write new xml file
tree.write(OUTFILE, encoding='utf-8')
