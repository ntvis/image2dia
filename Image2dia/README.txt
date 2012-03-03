=========
image2dia
=========

Introduction
=============
This is a console program (IDE & dia plugin are planed)


Installation
=============
It needs Python, of course, and the following python libraries:

  * cairo and rsvg: For SVG processing
  * lxml: For XML processing
  * Image: For image processing

Install the required libraries in Ubuntu is easy:

  $ sudo apt-get install python-rsvg python-cairo python-imaging python-lxml

It can also be instal·led with PyPi

  $ pip install image2dia

Execution
==========
From your program import the package and call the funcions

    >>> import image2dia
    >>> image2dia.image2dia("tempest.svg","")
    0
    
    

Example
=========

There are a sample in the 'bin' directory: 

    $ addImage2dia.py image.png sheet

where:

  * image.png: Is the name of the image
  * sheet: Is the sheet name where the image will be inserted

If some error occurs:

    $ ./addImage2dia.py image.png 
    image2dia.py v.0.4
    ---------------------------------
    Incorrect parameters
  
    The program needs two parameters:
     1) file name
     2) sheet name

   ex.  $ addImage2dia.py nom.png sheet


Example:

    $ addImage2dia.py Trash.svg Imatges
    addImage2dia.py v.0.4
    ---------------------------------
   Shape created 


  
  
