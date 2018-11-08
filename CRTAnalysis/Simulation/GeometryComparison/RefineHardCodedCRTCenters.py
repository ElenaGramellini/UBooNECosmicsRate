from ROOT import *
import os
import math
import argparse
import numpy as np
from array import array
import pprint 
import json
import itertools
from itertools import islice



### Create the block of text needed for output
def blockOfTextTemplate(febNumb, strip, x, y, z,  typeOfVolume):
    if typeOfVolume == 0:
        name1 = "volAuxDet_Module_" + str(febNumb) + "_strip_"+ str(strip)
        name2 = "posBMod_" + str(febNumb) + "_strip_"+ str(strip)
    elif typeOfVolume == 1:
        name1 = "volModule_" + str(febNumb) + "_strip_"+ str(strip)
        name2 = "posAMod_" + str(febNumb) + "_strip_"+ str(strip)
    elif typeOfVolume == -1:
        name1 = "volModule_" + str(febNumb) + "_strip_"+ str(strip)
        name2 = "posCMod_" + str(febNumb) + "_strip_"+ str(strip)

    line1 = "       <physvol>\n"
    line2 = "        <volumeref ref=\""  + name1 + "\"/>\n"
    line3 = "        <position name=\""  + name2 + "\" unit=\"cm\" x=\""+str(x)+"\" y=\""+str(y)+"\" z=\""+str(z)+"\"/>\n"
    line4 = "       </physvol>\n"

    return line1+line2+line3+line4


fnameGdml = "test.gdml"
dictionaryMCGdmlCenterStripA = {}
dictionaryMCGdmlCenterStripB = {}
dictionaryMCGdmlCenterStripC = {}

with open(fnameGdml, 'r') as f:
    for line in f.readlines():
        if "position" not in line:
            continue
        else:
            w  = line.split("\"")
            FEB   = mod2feb[int((w[1].split("_"))[1])]
            strip = int((w[1].split("_"))[3])
            uniquekey = 100*FEB+strip 
            centerPosX = float( w[5])
            centerPosY = float( w[7]) 
            centerPosZ = float( w[9]) 

            center = [centerPosX, centerPosY, centerPosZ]

            if "posAMod" in line:
                dictionaryMCGdmlCenterStripA[uniquekey] = center
            if "posBMod" in line:
                dictionaryMCGdmlCenterStripB[uniquekey] = center
            if "posCMod" in line:
                dictionaryMCGdmlCenterStripC[uniquekey] = center


for feb in mod2feb:
    for x in xrange(16):
        key = feb*100 + x

        original_CenterGdmlA = dictionaryMCGdmlCenterStripA[key]
        original_CenterGdmlB = dictionaryMCGdmlCenterStripB[key]
        original_CenterGdmlC = dictionaryMCGdmlCenterStripC[key]


        dicCorrectedCenterStripA [key] = original_CenterGdmlA  
        dicCorrectedCenterStripB [key] = original_CenterGdmlB
        dicCorrectedCenterStripC [key] = original_CenterGdmlC


alP = open("refinedHardCodedGeo.txt", "a")  
for feb in mod2feb:
    for x in xrange(16):
        key = feb*100 + x
        center = dicCorrectedCenterStripA [key] 
        line = blockOfTextTemplate(febNumberConversion(str(feb)), x, center[0], center[1], center[2],  1)
        alP.write(line)

for feb in mod2feb:
    for x in xrange(16):
        key = feb*100 + x
        center = dicCorrectedCenterStripB [key] 
        line = blockOfTextTemplate(febNumberConversion(str(feb)), x, center[0], center[1], center[2],  0)
        alP.write(line)

for feb in mod2feb:
    for x in xrange(16):
        key = feb*100 + x
        center = dicCorrectedCenterStripC [key] 
        line = blockOfTextTemplate(febNumberConversion(str(feb)), x, center[0], center[1], center[2],  -1)
        alP.write(line)






raw_input()  

