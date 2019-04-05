from xplnedsf import *
import os
import sys

def printInfo():
    print ("--------------------------------------------------------------------------")
    print ("                    XPLNEDSF kmlexport   version 0.01 (test)")
    print ("Exports mesh of an area of an dsf-file to a kml file.")
    print ("Usage: dsfVertexTool dsf-filename lat-S lat-N lon-W lon-E new-height")
    print ("       lan/lot coordinates of the area which should be exported.")
    print ("           new-height in meters")
    print ("Warning: This is still a test-version. No warrenties/guaranties!")
    print ("         Existing <inputfile>.kml files are overwritten!!!!!")
    print ("-------------------------------------------------------------------------")

try:
    filename = sys.argv[1]
    latS = float(sys.argv[2])
    latN = float(sys.argv[3])
    lonW = float(sys.argv[4])
    lonE = float(sys.argv[5])
except:
    printInfo()
    sys.exit()
    
filename = os.fspath(filename) #encode complete filepath as required by os

dsf = XPLNEDSF()
if dsf.read(filename): #returns value > 0 in case of errors
    sys.exit(1)

patchlist = dsf.PatchesInArea(latS, latN, lonW, lonE)

with open(filename + ".kml", "w") as f:
    f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
    f.write("<kml xmlns=\"http://www.opengis.net/kml/2.2\" >\n")
    f.write("<Document>\n")
    
    ############## Style definitions for Polygons in kml ###############
    f.write("<Style id=\"Water\"><LineStyle><width>1</width></LineStyle><PolyStyle><color>40ff0000</color></PolyStyle></Style>\n")
    f.write("<Style id=\"grass\"><LineStyle><width>1</width></LineStyle><PolyStyle><color>407fffaa</color></PolyStyle></Style>\n")
    f.write("<Style id=\"sand\"><LineStyle><width>1</width></LineStyle><PolyStyle><color>40f7ffff</color></PolyStyle></Style>\n")
    f.write("<Style id=\"ELSE\"><LineStyle><width>1</width></LineStyle><PolyStyle><color>4000aaaa</color></PolyStyle></Style>\n")
    f.write("<Style id=\"Area\"><LineStyle><color>ff0000ff</color><width>5</width></LineStyle><PolyStyle><fill>0</fill></PolyStyle></Style>\n")
    
    ########### Show selcted area in a rectangle ################
    f.write("    <Placemark><name>Selected Area</name><styleUrl>#Area</styleUrl><Polygon><outerBoundaryIs><LinearRing><coordinates>\n")
    f.write("        {2},{0},0 {2},{1},0 {3},{1},0 {3},{0},0 {2},{0},0\n".format(latS, latN, lonW, lonE))
    f.write("    </coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>\n")
    
    pcount = 0
    for p in patchlist:
        if p.flag == 1:
            flag = "PYS"
        else:
            flag = "OVL"
        terrain = dsf.DefTerrains[p.defIndex]
        if "Water" in terrain:
            style = "Water"
        elif "grass" in terrain:
            style = "grass"
        elif "sand" in terrain:
            style = "sand"
        else:
            style = "ELSE"
            
        f.write("<Folder><name>Patch {} ({}): {}</name>\n".format(pcount, flag, terrain))
        tcount = 0
        for t in p.triangles():
            f.write("    <Placemark><name>Tria {}</name><styleUrl>#{}</styleUrl><Polygon><outerBoundaryIs><LinearRing><coordinates>\n".format(tcount, style))
            v = dsf.TriaVertices(t)
            h = [] #stores heigth of vertices in triangles
            h.append(int(dsf.getElevation(v[0][0], v[0][1], dsf.V[t[0][0]][t[0][1]][2])))  #3rd Value is height from Vertex to be consideredn in case differnet from -32xxx
            h.append(int(dsf.getElevation(v[1][0], v[1][1], dsf.V[t[1][0]][t[1][1]][2])))
            h.append(int(dsf.getElevation(v[2][0], v[2][1], dsf.V[t[2][0]][t[2][1]][2])))
            f.write("        {0},{1},{2} {3},{4},{5} {6},{7},{8} {0},{1},{2}\n".format(v[0][0], v[0][1], h[0], v[1][0], v[1][1], h[1], v[2][0], v[2][1], h[2]))
            f.write("    </coordinates></LinearRing></outerBoundaryIs></Polygon></Placemark>\n")
            tcount += 1
        f.write("</Folder>\n")
        pcount += 1

    f.write("</Document></kml>\n")
    
