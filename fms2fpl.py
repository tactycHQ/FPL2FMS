#Script to convert Skyvector FPL files to X-Plane 11 FMS Flight Plans
import sys
from tkinter import *
from tkinter import filedialog
import xml.etree.ElementTree as ET

ident =[]
type = []
ccode =[]
lat = []
lon =[]

def OpenFile():
    root = Tk();root.withdraw()
    filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("fpl","*.fpl"),("all files","*.*")))
    f = open(filename)
    txt = f.read()
    f.close()
    return txt

def ParseXML():
    tree = ET.ElementTree(ET.fromstring(OpenFile()))
    root = tree.getroot()
    # print (root[1][1][1].tag)
    # print(root[1][1][1].text)
    print(root[1].tag.find('}')+1)
    wpl = [wpt.text for wpt in tree.iter() if wpt.tag == 'type']
    print(wpl)




ParseXML()