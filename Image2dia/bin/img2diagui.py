#!/usr/share/bin python
# -*- coding: UTF-8 -*-
import os
import wx
from lxml import etree 


class Img2diaGui(wx.App):
    def OnInit(self):
        self.tltle="Image2Dia Gui"
        self.frame = Img2DiaFrame(None, title="Image2Dia")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        
        return True


class Img2DiaFrame(wx.Frame):
    
    def __init__(self, parent, *args, **kwargs):
        super(Img2DiaFrame, self).__init__(parent, *args, **kwargs)
        
        self.panel = Img2DiaPanel(self)
                
        # Layout
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.panel, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.SetInitialSize()
               
        # self.button = wx.Button(self.panel, label="Push Me", pos=(50, 50))
        # self.botoID = self.button.GetId()
        # self.Bind(wx.EVT_BUTTON, self.Onbutton, self.button)
        
        # Window Size
#        mida = self.GetSize()
#        
#        self.botoOk = wx.Button(self.panel, wx.ID_OK)
#        self.botoOk.SetPosition((50,mida[1] - self.botoOk.GetSize()[1]))
#        self.botoOk = self.botoOk.GetId()
#        self.Bind(wx.EVT_BUTTON, self.OnOkl,self.botoOk)
#        
#        self.botoCancel = wx.Button(self.panel, wx.ID_CANCEL)
#        self.botoCancel.SetPosition((mida[0]-self.botoCancel.GetSize()[0]-10, mida[1] - self.botoCancel.GetSize()[1]))
#        self.botoCancel = self.botoCancel.GetId()
#        self.Bind(wx.EVT_BUTTON, self.OnCancel,self.botoCancel)
#        self._creaPantalla()


class Img2DiaPanel(wx.Panel):
    
    def __init__(self, parent, *args, **kwargs):
        super(Img2DiaPanel, self).__init__(parent, *args, **kwargs)
        
        #Atributs
        self.newSheet = wx.CheckBox(self,id=-1,label="New Sheet")
        self.textNewSheet = wx.TextCtrl(self) 
        self.newSheet.SetValue(False)
        self.Bind(wx.EVT_CHECKBOX, self.onNewSheetValue, self.newSheet)
        
        self.Bind(wx.EVT_TEXT, self.onEditTextNewSheet, self.textNewSheet)
        self.textNewSheet.Enabled=False
        
        self.sheets = wx.ComboBox(self)        
        self.Bind(wx.EVT_COMBOBOX, self.onComboBoxChange, self.sheets)
        
        
        # self.llistaImatges = wx.ImageList(self,22,22,True)
        self.llistaImatges = wx.ImageList(22,22,True)
        self.llista = wx.ListCtrl(self, -1, style=wx.LC_ICON | wx.LC_AUTOARRANGE)
        self.llista.InsertColumn( 0, "shapes", width=-1)
        self.llista.AssignImageList(self.llistaImatges, wx.IMAGE_LIST_NORMAL)
        self._loadSheets()        
        
        logodir = os.path.abspath("./clic.png")
        bitmap = wx.Bitmap(logodir, type=wx.BITMAP_TYPE_PNG)
        self.imatge = wx.StaticBitmap(self, bitmap=bitmap)
        self.Bind(wx.EVT_KEY_DOWN, self.onImatgeClicked, self.imatge)
        # Image File to 
        self._FinalimageFile = ""
        self._finalSheet = ""
        
        # Botons
        self.botoAfegeix = wx.Button(self,label="Add Image to Dia")
        self.botoAfegeix.Enabled=False
        self.Bind(wx.EVT_BUTTON, self.onBotoAfegeix, self.botoAfegeix)
        
        self.botoReset = wx.Button(self,label="Reset")
        self.Bind(wx.EVT_BUTTON,self.onBotoReset, self.botoReset)
        
        self.botoSortir= wx.Button(self,label="Exit")        
        self.Bind(wx.EVT_BUTTON, self.onBotoSortir, self.botoSortir)
        
        self.openFile = wx.Button(self,label="Select image")
        self.Bind(wx.EVT_BUTTON,self.onOpenFile, self.openFile)        
        
        self._creaPantalla()

    def _creaPantalla(self):
        ''' Genera la pantalla amb quadres ... si puc ''' 
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        sizerLogotip = wx.BoxSizer(wx.HORIZONTAL)
        sizerQuadres = wx.BoxSizer(wx.HORIZONTAL)
        sizerQuadres2 = wx.BoxSizer(wx.HORIZONTAL)
        sizerLlista = wx.BoxSizer(wx.HORIZONTAL)
        sizerBotons = wx.BoxSizer(wx.HORIZONTAL)
        sizerImatge = wx.BoxSizer(wx.VERTICAL)
        
        # Crear controls: Logo
        logodir = os.path.abspath("./image2dia.png")
        bitmap = wx.Bitmap(logodir, type=wx.BITMAP_TYPE_PNG)
        self.bitmap = wx.StaticBitmap(self,bitmap=bitmap)
        
        sizerLogotip.AddStretchSpacer(1)
        sizerLogotip.Add(self.bitmap,4, wx.ALIGN_CENTER_HORIZONTAL | wx.ALIGN_CENTER_VERTICAL)
        sizerLogotip.AddStretchSpacer(1)
        
        labelSheet = wx.StaticText(self, label="Sheets:")

        sizerQuadres.AddSpacer(15)
        sizerQuadres.Add(self.newSheet,2, wx.ALIGN_BOTTOM)
        sizerQuadres.AddStretchSpacer(4)
                
        sizerQuadres2.AddSpacer(15)
        sizerQuadres2.Add(self.textNewSheet,1, wx.ALIGN_CENTER_VERTICAL | wx.LEFT | wx.RIGHT)
        sizerQuadres2.AddStretchSpacer(1)
        sizerQuadres2.Add(labelSheet,1, wx.ALIGN_CENTER_VERTICAL | wx.ALIGN_RIGHT)
        sizerQuadres2.AddSpacer(2)
        sizerQuadres2.Add(self.sheets,3,wx.ALIGN_CENTER_VERTICAL)
        sizerQuadres2.AddSpacer(10)
        
        sizerImatge.AddSpacer(2)
        sizerImatge.Add(self.imatge,6, wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_CENTER_HORIZONTAL)
        sizerImatge.AddSpacer(2)
        sizerImatge.Add(self.openFile,1,wx.EXPAND)
        
        sizerLlista.AddSpacer(15)
        sizerLlista.Add(sizerImatge,2,wx.EXPAND)
        sizerLlista.Add(self.llista,4,wx.EXPAND)
        sizerLlista.AddSpacer(15)
         
        sizerBotons.AddStretchSpacer(2)
        sizerBotons.Add(self.botoAfegeix)
        sizerBotons.AddSpacer(10)
        sizerBotons.Add(self.botoReset)
        sizerBotons.AddSpacer(10)
        sizerBotons.Add(self.botoSortir)
        sizerBotons.AddStretchSpacer(2)
        
        vsizer1.AddSpacer(10)
        vsizer1.Add(sizerLogotip, 2, wx.EXPAND|wx.LEFT|wx.RIGHT,20)
        vsizer1.AddSpacer(10)
        vsizer1.Add(sizerQuadres, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        vsizer1.Add(sizerQuadres2, 1, wx.EXPAND | wx.LEFT | wx.RIGHT, 20)
        vsizer1.AddSpacer(10)
        vsizer1.Add(sizerLlista, 4, wx.EXPAND)
        vsizer1.AddSpacer(10)
        vsizer1.Add(sizerBotons,1, wx.EXPAND)
        vsizer1.AddSpacer(10)
        
        self.SetSizer(vsizer1)

    def _loadSheets(self):
        ''' 
           Load the sheets in the current installation
           
           Shapes not allways have the same name of the sheets 
           I need to see the 'name' tag to discover it! 
        
        ''' 
        print "..Loading sheets"
        DIA_DIR = "{0:>s}/.dia".format(os.path.expanduser("~"))
        for fitxer in os.listdir(DIA_DIR+"/sheets"):
            nom,_ = os.path.splitext(fitxer)
            # Test if the shape folder  is the same... if not I need discover it 
            # with the <name> tag ...
            self.sheets.Append(nom)

        self.sheets.SetSelection(0)
        self._loadImatges(0)
        
    def _loadImatges(self,position):
        ''' Load Icons to the ListCtrl  an to list ''' 
        sheet = self.sheets.GetValue()
        
        DIA_DIR = "%s/.dia/" % (os.getenv("HOME"))
        self.fitxers = []
        # self.llista.ClearAll()
        self.llistaImatges.RemoveAll()
        self.llista.ClearAll()
        
        Error = False
        
        sheetFile = DIA_DIR + "sheets/%s.sheet" % (sheet)        
        shapeDir = DIA_DIR + "shapes/%s/" % sheet
        
        if not os.path.isdir(shapeDir):
            # I will try the sheet references ... with XPath
            xpathTries = [ "//d:name/text()", "//d:object/@name"]
            root = etree.parse(sheetFile)
            Error = True
            for index, xpt in enumerate(xpathTries):
                # Test if the folder is in the name...
                sheet = root.xpath(xpt,
                                   namespaces={'d': 'http://www.lysator.liu.se/~alla/dia/dia-sheet-ns'})[0]        
                if index==1: 
                    sheet, _ = sheet.split(" - ",1)
                    
                shapeDir = DIA_DIR + "shapes/%s/" % (sheet)                 
                if os.path.isdir(shapeDir):
                    Error=False
                    break;
        
        if Error == False:            
            for fitxer in os.listdir(shapeDir):                
                if os.path.splitext(fitxer)[1] == ".shape":                     
                    shapeFile = shapeDir + fitxer
                    resultat = []
                    try:              
                        root = etree.parse(shapeFile)
                        resultat = root.xpath("//d:icon/text()",
                                          namespaces={'d': 'http://www.daa.com.au/~james/dia-shape-ns'})      
                    except IOError:
                        print "... %s not found" % shapeFile
                    
                    if len(resultat)==1:                     
                            bmp = wx.Bitmap(shapeDir+resultat[0], wx.BITMAP_TYPE_PNG)               
                            il_max = self.llistaImatges.Add(bmp)
                            self.fitxers.append(resultat[0])
                
        for x, fitxer in enumerate(self.fitxers):
            img = x % (il_max+1)
            #self.llista.InsertImageStringItem(x, fitxer, img)
            self.llista.InsertImageStringItem(x,str(x),img)        
                            
    def onBotoAfegeix(self,event):
        print "Pressed 'Add'"
        
    def onBotoSortir(self,event):
        ''' Exit ''' 
        print "exit"
        wx.Exit()
    
    def onBotoReset(self,event):
        ''' Reset ''' 
        self._loadSheets()
        print "reset"
    
    def onOpenFile(self, event):
        ''' Select the file to be inserted on Dia ''' 
        
        filters = 'Image files (*.gif; *.png; *.jpg; *.svg) | *.gif;*.png;*.jpg;*.svg'
        dialeg = wx.FileDialog(self,message="Select the Image...", 
                                          defaultDir=os.getcwd(), 
                                          defaultFile="", 
                                          wildcard=filters, 
                                          style=wx.OPEN)
        
        if dialeg.ShowModal() == wx.ID_OK:
            nom = dialeg.GetPath()
            # bitmap = wx.Bitmap(nom, type=wx.BITMAP_TYPE_PNG)
            bitmap = wx.Image(nom,type=wx.BITMAP_TYPE_ANY).Rescale(self.imatge.GetSize()[0],self.imatge.GetSize()[0] ) .ConvertToBitmap()
            self.imatge.SetBitmap(bitmap)
            self.imatge.Fit()
            self._FinalimageFile = dialeg.GetPath()
            
            self._checkAllOk()
        
        dialeg.Destroy() 

    def _checkAllOk(self):
        if self.newSheet.GetValue() == True:
            self._finalSheet = self.textNewSheet.GetValue()
            if self._finalSheet:
                self.botoAfegeix.Enable()
            else:
                self.botoAfegeix.Disable()
        else:
            if self._FinalimageFile > 0:
                self.botoAfegeix.Enable()
            else:
                self.botoAfegeix.Disable()
                
    def onEditTextNewSheet(self,event):
        self._finalSheet = self.textNewSheet.GetValue()
        self._checkAllOk()
                    
    def onNewSheetValue(self,event):
        ''' Enable or disable the controls for new Sheet or old Sheet ''' 
                
        if self.newSheet.GetValue() == True:            
            self.textNewSheet.Enabled=True
            self.sheets.Enabled=False
            self.llista.Enabled=False
            
        else:            
            self.textNewSheet.Enabled=False
            self.sheets.Enabled=True
            self.llista.Enabled=True
            self._loadImatges(0)
        self._checkAllOk()
            
    def onImatgeClicked(self,event):
        print "desafortunat"
    
    def onComboBoxChange(self,event):
        self._loadImatges(0)


def SetClipboardText(text):
    """Put text in the clipboard
    @param text: string
    """
    data_o = wx.TextDataObject()
    data_o.SetText(text)
    if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
        wx.TheClipboard.SetData(data_o)
    wx.TheClipboard.Close()

def GetClipboardText():
    """Get text from the clipboard
    @return: string
    """
    text_obj = wx.TextDataObject()
    rtext = ""
    if wx.TheClipboard.IsOpened() or wx.TheClipboard.Open():
        if wx.TheClipboard.GetData(text_obj):
            rtext = text_obj.GetText()
        wx.TheClipboard.Close()
    return rtext
    


if __name__ == "__main__":
    app = Img2diaGui(False)
    app.MainLoop()
