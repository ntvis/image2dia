#Ubuntu installation

# Introduction #
This is a console program (IDE & dia plugin are planed). To use Image2Dia you need to install some Python libraries:

  * cairo and rsvg: For SVG processing
  * lxml: For XML processing
  * Image: For image processing

Installing the required libraries in Ubuntu is easy:

```
  $ sudo apt-get install python-rsvg python-cairo python-imaging python-lxml
```

# Installation #
You can download the package but a best solution (distribution independent) is install it via PyPi:

```
  $ sudo pip install image2dia
```
You can need to install the package **python-pip**

# Execution #
From your program import the package and call the funcions

```
    >>> import image2dia
    >>> image2dia.image2dia("tempest.svg","Weather")
    0
```

# Example #
There are a sample script in the 'bin' directory named **addImage2dia**:
```
    $ addImage2dia.py image.png sheet
```

where:

  * image.png: Is the name of the image
  * sheet: Is the sheet name where the image will be inserted

If some error occurs:
```
    $ ./addImage2dia.py image.png 
    image2dia.py v.0.4
    ---------------------------------
    Incorrect parameters
  
    The program needs two parameters:
     1) file name
     2) sheet name

   ex.  $ addImage2dia.py nom.png sheet
```

Example:

```
    $ addImage2dia.py Trash.svg Imatges
    addImage2dia.py v.0.4
    ---------------------------------
   Shape created 
```


