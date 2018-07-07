#Script to convert Skyvector FPL files to X-Plane 11 FMS Flight Plans
import sys
from tkinter import *
from tkinter import filedialog
import xml.etree.ElementTree as ET

#Creating dictionary for Special Column
tdict = {"AIRPORT":1,"NDB":2,"VOR":3,"INT":11}

#OpenFile method opens the FPL file and returns the route name and raw text
def OpenFile():
    root = Tk();root.withdraw()
    filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("fpl","*.fpl"),("all files","*.*")))
    f = open(filename)
    txt = f.read()
    f.close()
    return filename,txt

#ParseXML method parses the text string from the OpenFile method and returns data lists to be used to generate FMS
def ParseXML():
    ident = []
    type = []
    ccode = []
    lat = []
    lon = []
    fn,txt = OpenFile()
    tree = ET.ElementTree(ET.fromstring(txt))
    root = tree.getroot()
    nspc = root.tag[0:root.tag.find("}")+1]

    for wpt in root[1].findall(nspc+"waypoint"):
        ident.append(wpt.find(nspc+"identifier").text)
        type.append(wpt.find(nspc + "type").text)
        ccode.append(wpt.find(nspc + "country-code").text)
        lat.append(wpt.find(nspc + "lat").text)
        lon.append(wpt.find(nspc + "lon").text)
    return ident,type,ccode,lat,lon,fn

#createFMS method inputs the data lists from ParseXML to return FMS file
def createFMS (ident,type,ccode,lat,lon,fmsname):
    if len(ident)==len(type)==len(ccode)==len(lat)==len(lon):
        print("Generated arrays of same length succesfully")

    fmsname=fmsname[0:fmsname.find(".")]

    #Following code is implementing logic for FMS file format from here: https://developer.x-plane.com/article/flightplan-files-v11-fms-file-format/
    out = ""
    header="I\n1100 Version\nCYCLE 1805\n"
    adep = "ADEP "+i[0]+"\n"
    ades = "ADES "+i[len(i)-1]+"\n"
    numenr="NUMENR "+str(len(i))+"\n"
    out = header + adep + ades + numenr

    for count,t in enumerate(type):
        special = ""
        if count==0:
            special = "ADEP"
        elif count==len(type)-1:
            special = "ADES"
        else:
            special = "DRCT"

        out=out+str(tdict[t])+" "+str(ident[count])+" "+special+" 0.000000 "+lat[count]+" "+lon[count]+"\n"

    #Creating and writing to FMS file the string "out"
    fms_file=open(fmsname+".fms","w")
    fms_file.write(out)
    fms_file.close()
    print("FMS generated successfully")

#Runtime
i,t,c,lt,ln,fn = ParseXML()
createFMS(i,t,c,lt,ln,fn)