from xplnedsf import *
import os
import sys

def printInfo():
    print ("--------------------------------------------------------------------------")
    print ("                     XPLNEDSF Vertex Tool   version 0.1 (test)")
    print ("Changes height of vertices in an area directly in an X-Plane DSF File")
    print ("Usage: dsfVertexTool dsf-filename lat-S lat-N lon-W lon-E new-height")
    print ("       lan/lot coordinates of the area where vertices are set to")
    print ("           new-height in meters")
    print ("       Input-file is saved with ending .org")
    print ("Warning: This is still a test-version. No warrenties/guaranties!")
    print ("         Existing .org files are overwritten!!!!!")
    print ("-------------------------------------------------------------------------")

try:
    filename = sys.argv[1]
    latS = float(sys.argv[2])
    latN = float(sys.argv[3])
    lonW = float(sys.argv[4])
    lonE = float(sys.argv[5])
    newheight = int(sys.argv[6])
except:
    printInfo()
    sys.exit()
    
filename = os.fspath(filename) #encode complete filepath as required by os


dsf = XPLNEDSF()
if dsf.read(filename): #returns value > 0 in case of errors
    sys.exit(1)

for p in dsf.V:  #for all pools
    for v in p: #go through all vertices
        if len(v) >= 5: #vertices whith less than 5 coordinates are not used for mesh
            if lonW <= v[0] <= lonE:
                if latS <= v[1] <= latN:
                    print ("Adapt height for vertex:", v)
                    v[2]=newheight
                    
try:
   os.replace(filename, filename + ".org")
except:
   print('Error:', filename, 'can not be replaced!')
   sys.exit(0)
   
dsf.write(filename)
