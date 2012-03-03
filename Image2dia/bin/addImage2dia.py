#!/usr/bin/env python
import os
import sys
from image2dia import Image2Dia

def Error(nom):
    """ 
    Error detected, show usage options 
    
    PARAMS
       nom: executable name
    """
    print """The program needs two parameters:

       1) file name
       2) sheet name

       ex.  $ {0:>s} name.png sheet
       """.format(os.path.basename(nom))


# -- MAIN -- 
i2d = Image2Dia()
# Always show the version info
print "%s v.%s" % (os.path.basename(sys.argv[0]), i2d.getVersion())
print "-----------------------------------"
    
# Check params
if len(sys.argv) == 3:
    nomfitxer = sys.argv[1]
    grup = sys.argv[2]
    resultat = i2d.addImage(nomfitxer,grup)
else:
    resultat = 1
           
print ""
if resultat != 0:
    Error(sys.argv[0])
        
