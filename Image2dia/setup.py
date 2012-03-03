
from setuptools import setup

setup(
    name="Image2Dia", 
    version="0.51", 
    description="Insert images into diagram editor Dia",
    author="Xavier Sala (utrescu)",
    url="http://code.google.com/p/image2dia/",
    license="GPL",
    packages=['image2dia'],
    scripts=['bin/addImage2dia.py']
#    install_requires=[ 
#        "pycairo",
#	"lxml",
#	"rsvg",
#	"PIL"],
)

