#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
'''
 The main function of this object is to add images (png, jpg, svg, ...) 
 into a DIA sheets

  * Inserts an image to a DIA sheet. For do it creates the
  22x22 icon, a XML  shape file, copy the file into the appropiate
  folder and adds a referencie into the sheet file 
  (If the sheet file does not exists it is created)

  VERSIONS
* 0.51 
   - Investigating how to automatically import the class
   
* 0.5
  - Converted Image2Dia to a class. 
  - Changed home user path to be portable to Windows
  - Added functions to list sheets 
  - Reordering the code
  - Solved problems with transparencies in icons

 * 0.41, 0.42
   - Problems with PyPi setup...

 * 0.4
   - Little changes in messages and comments
   - Reorder the code to create a Python package 
     - Added a class to handle errors
     - Added sample
   - Added documentation and comentaries
   - 
  
 * 0.3
    - Script modified to be embedable
 
 * 0.2
    - Corrected some messages
    - fixed problems creating a directory
    - Tests if insertion will create duplicate reference names of the shape
      in sheet before inserting
    - Automatic creation of shape folder
    - Automatic creation of sheet file
    - Tests shapes and sheets existence
    - Creates five connection points (top-left, top-right, middle,
                                      bottom-left, bottom-right)

 * 0.09
    - Write Sheet file (testing)
    - Translated messages and comments to English

 * 0.01
      - Shape file creation, icon creation and copying file in shape folder
      - Works with SVG images (converts to a PNG to create the icon)
      - Creates diagonal poings
      - Does not modify sheet file (only shows the line on the screen)


                     Xavier Sala
'''

import os
import sys
try: 
    from lxml import etree
    import Image
    import shutil
    import cairo
    import rsvg
except:
    print """ERROR:
    Some dependencies failed"
    
        cairo, rsvg, PIL and lxml needed"
    """


class Image2Dia():
    '''
    This class inserts an image file into an DIA sheet.
     
     The main function is 'add(filename,sheet)'
    '''
    
    # CONSTANTS ...     
    VERSIO = "0.51"
    
    _SHEET_LINE = """<object name='%s - %s'><description>%s</description></object>"""
    _SHEET_NS = "{http://www.lysator.liu.se/~alla/dia/dia-sheet-ns}"
    
    _SHAPE_NS = "{http://www.daa.com.au/~james/dia-shape-ns}"    
    _SVG_NS = "{http://www.w3.org/2000/svg}"
    _XLINK_NS = "{http://www.w3.org/1999/xlink}"    
    
    
    class Image2DiaErrors(Exception):
        '''
        Class to manage errors generated with Image2dia
        
        0: Shape created without problems
        1: Incorrect parameters
        2: Image file allready in this sheet
        3: Name of the shape allready in use in the same sheet
        4: Image file provided not found
        '''
        errors = [ 
                       "Shape created", 
                       "Incorrect parameters", 
                       "Image file allready in use in this sheet", 
                       "The name of the shape is allready in use in the specified sheet", 
                       "Image file not found", 
                       ]
        def __init__(self,value):
            self.value = value
            
        def __str__(self):
            return self.errors[self.value]
        
    
    def __init__(self):
        self.DiaUserDir = "{0:>s}/.dia".format(os.path.expanduser("~"))
    
    def getVersion(self):
        ''' 
        returns the version of the module
        '''
        return self.VERSIO
    
    
    def _getDiaUserDir(self):
        return self.DiaUserDir
    
    def _getSheetsDir(self,p):
        '''
        Returns the sheets directory
        
        PARAMS
            USER: User directory
            SYSTEM: System directory (not working in non Debian systems)
        '''
        SHEETS_DIR = { "USER" :  "{0:>s}/sheets".format(self._getDiaUserDir()), 
                                 "SYSTEM" : "/usr/share/dia/sheets" }
        if p in SHEETS_DIR:
            return SHEETS_DIR[p]
        else:
            return None
        
    def _getShapesDir(self, p):
        '''
        Returns the shapes dir
        
        PARAMS
            USER: User directory
            SYSTEM: System directory (not working in non Debian systems)        
        '''
        SHAPES_DIR = { "USER" : "{0:>s}/shapes".format(self._getDiaUserDir()), 
                                 "SYSTEM" : "/usr/share/dia/shapes"}
        if p in SHAPES_DIR:
            return SHAPES_DIR[p]
        else:
            return None
    
    def listSheets(self, quin):
        ''' 
        Gives a list with the actual Sheets in the local installation
        
        PARAMS
             quin: Must be USER or SYSTEM 
                        USER: Sheets in the user home folder
                        SYSTEM: Sheets of the system  (only /usr/share/dia )
                        
            returns the specified list or an empty list for incorrect parameters           
        '''
        newList = []    
        directori = self._getSheetsDir(quin)
    
        if directori is not None:       
            for fitxer in os.listdir(directori):
                nom,_ = os.path.splitext(fitxer)
                newList.append(nom)
                
        return newList
    
    
    def listAllSheets(self):
        '''
        Returns all sheets in the system
        '''
        newList = []
        for value in ("USER","SYSTEM"):
            newList = newList + self.listSheets(value)
            
        return newList
    
    def _createDiaSheetFile(self, nom):
        """
        Create a new Sheet file
        
        PARAMS
           nom: Name of the sheet      
        """
        
        sheet = """<?xml version="1.0" encoding="utf-8"?>
        <sheet xmlns="http://www.lysator.liu.se/~alla/dia/dia-sheet-ns">
        <name>Imatges</name>
        <description>Simplement imatges</description>
        <contents>
        </contents>
        </sheet>
        """    
    
        root = etree.XML(sheet)
    
        description, _ = os.path.splitext(os.path.basename(nom))
    
        for element in root.iter():
            if element.tag == self._SHEET_NS + 'name':
                element.text = description
            elif element.tag == self._SHEET_NS + 'description':
                element.text = description
    
        doc = etree.ElementTree()
        doc._setroot(root)
        doc.write(nom, encoding="utf-8", xml_declaration=True, method="xml")    
    
    def _createDiaShapeFile(self, shapeFile, grup, nomfitxer, mida):
        '''
        Creates a shapeFile with the name especified
        
        PARAMS
            shapefile: Name of the shape File
            grup: Sheet name
            nom: Name of the shape
            mida: List with the dimensions of the image
        '''
    
        shape = """<?xml version="1.0" encoding="UTF-8"?>
        <shape xmlns="http://www.daa.com.au/~james/dia-shape-ns"
               xmlns:svg="http://www.w3.org/2000/svg"
               xmlns:xlink="http://www.w3.org/1999/xlink">
        <name>Imatges - Tux</name>
        <icon>tux-icon.png</icon>
        <connections>
        <point x="0" y="0"/>
        <point x="0" y="20"/>
        <point x="10" y="10"/>
        <point x="20" y="0"/>
        <point x="20" y="20"/>
        </connections>
        <aspectratio type="fixed"/>
        <svg:svg>
        <svg:image x="0" y="0" width="20" height="20" xlink:href="tux.png"/>
        </svg:svg>
        </shape>
        """    
        
        nom, _ = os.path.splitext(nomfitxer)
        
        root = etree.XML(shape)
        for element in root.iter():
            if element.tag == self._SHAPE_NS + 'name':
                element.text = grup + " - " + nom
            elif element.tag == self._SHAPE_NS + 'icon':
                element.text = '%s-icon.png' % (nom)
            elif element.tag == self._SHAPE_NS + 'connections':
                x = 0
                y = 0
                # iterx = midax / (len(element)-1)
                # itery = miday / (len(element)-1)
                for fill in element.iterchildren():
                    if element.index(fill) == 0:
                        x = mida[0] / 2
                        y = mida[1] / 2
                        fill.set('x', str(x))
                        fill.set('y', str(y))
                        x = 0
                        y = 0
                    else:
                        if x > mida[0]:
                            x = 0
                            y = y + mida[1]
                        fill.set('x', str(x))
                        fill.set('y', str(y))
                        x = x + mida[0]
        
            elif element.tag == self._SVG_NS + 'image':
                    element.set("%shref" % (self._XLINK_NS), nomfitxer)
                    element.set('width', str(mida[0]))
                    element.set('height', str(mida[1]))
            
        # Write shape file
        '''
         1) If I use parse() I can write it to screen
            doc.write(sys.stdout)        
        2) Same but starting from root element
            print etree.tostring(root, xml_declaration=True,
            encoding="UTF-8",pretty_print=True)
        '''        
        doc = etree.ElementTree()
        doc._setroot(root)
        doc.write(shapeFile, encoding="UTF-8", xml_declaration=True, method="xml")       
    
    
    def checkFiles(self, shapeFile, sheetFile):
        """
        1- Test if the shape file exists (for not overwriting existing shapes)
        2- Test if the sheet File already exists 
    
        PARAMS       
           shapeFile: Name of the shape file (full path)
           sheetFile: Name of the sheet where the shape will be inserted 
                         (full path)
           
        RETURNS
           0: Ok
           1: Reserved
           2: Shape file allready exists
           3: Shape allready in the sheet
        """
        # Check if the shape file exists:
        if os.path.exists(shapeFile):
            raise self.Image2DiaErrors(2)
            
        # Check if we are adding a shape in an existent sheet
        if os.path.exists(sheetFile):
            # Name of the shape in the sheet file ("sheet - Name")
            shapeName = '%s - %s' % (os.path.basename(shapeFile),os.path.basename(sheetFile))
            # Test if the reference file already exists in the sheet -  XPath
            arrel = etree.parse(sheetFile, parser=None, base_url=None).getroot()
            r = arrel.xpath("//d:object/@name",
            namespaces={'d': 'http://www.lysator.liu.se/~alla/dia/dia-sheet-ns'})
            if shapeName in r:
                raise self.Image2DiaErrors(3)
        return 0
    
    def _convertSVGImageFile(self, nom):
        '''  
       Convesion from SVG to a PNG with the same name 
        '''        
        nomfitxer = "%s.svg" % (nom)
        svg = rsvg.Handle(nomfitxer)
        midax = svg.get_property('width')
        miday = svg.get_property('height')
            
        surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, midax, miday)
        ctx = cairo.Context(surface)
        svg.render_cairo(ctx)        
        surface.write_to_png(nom + ".png")        
        surface.finish()
    
    def _createIcon(self, nom, extensio):        
        ''' Creates an Icon for the shape 
        
          PARAMETERS
             nom      :  Name of the file without extension
             extensio: Extension 
             
          RETURNS
             Returns (sizex, sizey)
        '''        
        # create an icon 22x22 WITHOUT TRANSPARENCY             
        try:
            img = Image.open(nom + extensio)
        except:
            # Yes, I need to detect the error type ... maybe in the next version
            raise self.Image2DiaErrors(4)
            
        midax, miday = img.size   
        # Create a white background to skip 'bad transparency effect'
        icona = Image.new("RGB",(22,22),(255,255,255))     
        # Aspect Ratio
        novaMida = (30, 30 *miday/midax)
        img.thumbnail([22, 22], Image.ANTIALIAS)
        elformat = img.format
        
        center = ( (22 - img.size[0])/2, (22-img.size[1])/2 )
        icona.paste(img, center, img)
        
        try:
            icona.save('{0:>s}-icon.png'.format(nom), elformat, quality=90, optimize=1)
        except:
            icona.save("{0:>s}-icon.png".format(nom), elformat, quality=90)
            
        # img.close            
        return novaMida
    
    def addImage(self, nomfitxer, grup):      
        '''
        Inserts the image into the specified sheet. If the sheet
        does not exists its automaticaly created
    
        PARAMS
           nomfitxer: Image file name
           grup: Sheet to insert the image
        
        RETURN
           0: Shape created without problems
           
        RAISES
           Image2DiaErrors.
        '''            
        # Split name and extension
        nom, extensio = os.path.splitext(nomfitxer)
    
        # Define folders and files...
        shapeDir = self._getShapesDir("USER")
        sheetDir = self._getSheetsDir("USER")
        
        shapeFile = "{0:>s}/{1:>s}/{2:>s}.shape".format(shapeDir, grup, nom)
        sheetFile = "{0:>s}/{1:>s}.sheet".format(sheetDir, grup)
        
        
        # Test if the shape and sheet files are ok:    
        resultat = self.checkFiles(shapeFile, sheetFile)
    
        # 1) Icon creation
        # -------------------------------------------------------------
        # Must convert a SVG file to PNG to create an icon (Can be simplified?)
        if extensio == ".svg":
            self._convertSVGImageFile(nom) 
            extensio = ".png"
        
        mida =  self._createIcon(nom, extensio)
        
        # 2) Create the XML shape file
        # --------------------------------------------------------------
        folder = os.path.dirname(shapeFile)
        if not os.path.isdir(folder):            
            os.mkdir(folder, 0750)                
        # Create the file
        self._createDiaShapeFile(shapeFile, grup, nomfitxer,mida)
            
        # 3) Add the new image to sheets file
        # -------------------------------------------------
        if not os.path.exists(sheetFile):
            # Sheet not found, proceed creating one ... 
            self._createDiaSheetFile(sheetFile)
            
        doc = etree.parse(sheetFile)
        node = doc.find("%scontents" % (self._SHEET_NS))
        # Insert the new node
        noufill = etree.XML(self._SHEET_LINE % (grup, nom, nom))
        node.append(noufill)
        doc.write(sheetFile, encoding="utf-8", xml_declaration=True, method="xml") 
                    
        # 4) Copy the images into the shape folder
        # -------------------------------------       
        shapeDestination = "%s/%s" % (shapeDir, grup)   
        if os.getcwd() != shapeDestination:
            shutil.copy2(nomfitxer, shapeDestination)
            shutil.move("%s-icon.png" % (nom), shapeDestination)
            
        # Happy End
        return resultat


if __name__ == "__main__":
    # Always show the version info
    i2d = Image2Dia()
    print "%s v.%s" % (os.path.basename(sys.argv[0]), i2d.getVersion())
    print "-----------------------------------"
    
    nomfitxer = ""
    
    # 0) Check params
    # -------------------------------------
    if len(sys.argv) == 3:
        nomfitxer = sys.argv[1]
        grup = sys.argv[2]
        resultat = i2d.addImage(nomfitxer,grup)
    else:
        raise i2d.Image2DiaErrors(1)
            

        
    
