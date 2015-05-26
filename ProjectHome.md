![http://personal.telefonica.terra.es/web/utrescu/image2dia/img2dia.png](http://personal.telefonica.terra.es/web/utrescu/image2dia/img2dia.png)

# Objectives #
The goal is to automatically insert images (PNG, JPG, SVG, ...) in sheets of the Diagram editor DIA http://projects.gnome.org/dia/.


## Why? ##
I sometimes needs more pleasant pictures in my diagrams and the best solution is to add pictures in PNG or SVG format. Drag & drop works well with bitmap images but frequently does not work with SVG pictures (the result can be horrible).

![http://personal.telefonica.terra.es/web/utrescu/image2dia/case.png](http://personal.telefonica.terra.es/web/utrescu/image2dia/case.png)

But I have seen that loading SVG files through a shape works perfectly

The script:

  * Creates shapes for the images using the **custom shape module** http://projects.gnome.org/dia/custom-shapes
  * Creates the icon
  * Copies the image in the apropiate folder
  * Inserts the new shape in the refered sheet (creates it if needed)
  * Defines five connection points in the new shape

![http://personal.telefonica.terra.es/web/utrescu/image2dia/example.png](http://personal.telefonica.terra.es/web/utrescu/image2dia/example.png)


### GUI ###
I'm also working on a GUI based on wxPython. It's not available yet

![http://personal.telefonica.terra.es/web/utrescu/image2dia/Image2Diagui.png](http://personal.telefonica.terra.es/web/utrescu/image2dia/Image2Diagui.png)


### Future ###

In the future I'm plannig to:
  * Create a Dia plugin

## Python ##
This project is also used to learn Python. It is my first program in Python (though I have programming experience) so I hope it will improve as I learn the language
