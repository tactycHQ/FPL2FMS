#Script to convert Skyvector FPL files to X-Plane 11 FMS Flight Plans
import sys
from tkinter import *
from tkinter import filedialog
import xml.etree.ElementTree as ET


def OpenFile():
    root = Tk();root.withdraw()
    # filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("fpl","*.fpl"),("all files","*.*")))
    filename = 'KORD.fpl'
    f = open(filename)
    txt = f.read()
    f.close()
    return txt

def ParseXML():
    ident = []
    type = []
    ccode = []
    lat = []
    lon = []
    tree = ET.ElementTree(ET.fromstring(OpenFile()))
    root = tree.getroot()
    nspc = root.tag[0:root.tag.find("}")+1]

    for wpt in root[1].findall(nspc+"waypoint"):
        ident.append(wpt.find(nspc+"identifier").text)
        type.append(wpt.find(nspc + "type").text)
        ccode.append(wpt.find(nspc + "country-code").text)
        lat.append(wpt.find(nspc + "lat").text)
        lon.append(wpt.find(nspc + "lon").text)
    return ident,type,ccode,lat,lon

def createFMS (ident,type,ccode,lat,lon):
    header="I\n1100 Version"
    out =""
    print(header)


#Runtime
i,t,c,lt,ln = ParseXML()
createFMS(i,t,c,lt,ln)