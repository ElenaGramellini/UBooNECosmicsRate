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
import collections



# Put here the general transformation of coordinante
def gdmlOffSet():
    return 128.75 , 0., 518.5


def next_n_lines(file_opened, N):
    return [x.strip() for x in islice(file_opened, N)]

### Create the block of text needed for output
def blockOfTextTemplate(febNumb, strip, x, y, z, rotationTag, typeOfVolume):
    if typeOfVolume == 0:
        name1 = "volAuxDet_Module_" + str(febNumb) + "_strip_"+ str(strip)
        name2 = "posAuxDet_Module_" + str(febNumb) + "_strip_"+ str(strip)
    elif typeOfVolume == 1:
        name1 = "volModule_" + str(febNumb) + "_strip_"+ str(strip)+"_10"
        name2 = "posModule_" + str(febNumb) + "_strip_"+ str(strip)+"_10"
    elif typeOfVolume == -1:
        name1 = "volModule_" + str(febNumb) + "_strip_"+ str(strip)+"_01"
        name2 = "posModule_" + str(febNumb) + "_strip_"+ str(strip)+"_01"

    line1 = "       <physvol>\n"
    line2 = "        <volumeref ref=\""  + name1 + "\"/>\n"
    line3 = "        <rotationref ref=\""+ rotationTag + "\"/>\n"
    line4 = "        <position name=\""  + name2 + "\" unit=\"cm\" x=\""+str(x)+"\" y=\""+str(y)+"\" z=\""+str(z)+"\"/>\n"
    line5 = "       </physvol>\n"

    return line1+line2+line3+line4+line5



### Given the FEB name, tell me the febNumb
def febNumberConversion( febName = "11"):
    mod2feb = [ 24,23,22,17,14,18,19,12,11,52,
                31,29,28,27,26,30,61,59,57,60,
                58,56,32,38,36,35,34,33,37,45,
                44,43,42,41,40,39,55,54,53,51,
                49,47,21,16,50,48,46,20,15,107,
                106,105,109,108,112,111,195,123,124,125,
                126,129,115,114,113,116,119,121,127,128,
                117,120,118]

    mod2febDict = {}
    for i in xrange(0,73):
        mod2febDict[mod2feb[i]] = i

    return mod2febDict[int(febName)]





### Given the FEB name, tell me the module lenght
def febLenght( febName = "11"):
    striplength = [ 346.0, 346.0, 346.0, 259.6, 259.6, 259.6, 259.6, 227.0, 227.0, 346.0,
                    346.0, 346.0, 346.0, 346.0, 346.0, 346.0, 403.8, 403.8, 403.8, 403.8,                    
                    403.8, 403.8, 259.6, 259.6, 259.6, 259.6, 259.6, 259.6, 259.6, 259.6,                                                                 
                    259.6, 259.6, 259.6, 259.6, 259.6, 259.6, 396.2, 396.2, 396.2, 227.0,                                                              
                    227.0, 227.0, 227.0, 227.0, 227.0, 227.0, 227.0, 227.0, 227.0, 360.0,                                                               
                    360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 180.0, 180.0, 180.0, 180.0,                                                           
                    180.0, 180.0, 365.0, 365.0, 365.0, 365.0, 365.0, 365.0, 180.0, 180.0,                                 
                    365.0, 365.0, 365.0]
    
    index = febNumberConversion(febName)
    return striplength[index]



def findRotationTag(febNumb = 1):
    # Read the gdml, 
    #find the rotation tag corresponding to this FEB, 
    #return it
    fnameGdml = "gdml/CRTTxt/p1.txt"
    with open(fnameGdml, 'r') as sample:
        notFound = True 
        name = "volAuxDet_Module_"+str(febNumb)
        while notFound:
            lines = next_n_lines(sample, 5)
            if name in lines[1]:
                notFound = False
                rotationTag = (lines[3].split("\""))[1]
                return rotationTag            
    return "pppp"



# prepare outgoin block of text
def prepareBlock(febkey = "1100", centers=[0,0,0], typeOfVolume = 0):
    febName     = febkey[:-2]
    febNumb     = febNumberConversion(febName)
    strip       = str(int(febkey[-2:]))

    offSet = gdmlOffSet()
    x           = centers[0] - offSet[0]
    y           = centers[1] - offSet[1]
    z           = centers[2] - offSet[2]
    rotationTag = findRotationTag(febNumb) 

    return  blockOfTextTemplate(febNumb, strip, x, y, z, rotationTag, typeOfVolume), febNumb



def calculateTxtCenters():
    # Given the FEB, do I need to add or subtract the lenght?
    plusFEBs  = [ 119, 120, 121, 109, 105, 106, 107, 125, 126, 128, 129, 119, 120, 121,
                  14,  17,  11,  12,  52,  31,  29,  28,  27,  26,  30,  39,  40,  41, 
                  42,  43,  44,  45 ]
    

    minusFEBs = [ 113, 114, 115, 116, 117, 118, 127, 195, 123, 124, 108, 112, 111,  22,
                  23,  24,  19,  18,  60,  61,  58,  59,  56,  57,  37,  33,  34,  32, 
                  35,  36,  38,  53,  54,  55,  15,  16,  20,  21,  46,  47,  48,  49, 
                  50,  51]
    signDict = {}
    for i in plusFEBs:
        signDict[str(i)] = 1.
    for i in minusFEBs:
        signDict[str(i)] = -1.

    # This is dictionary is our final result:
    # For each strip, we're going to fill it with
    # The strip center
    dictionaryDataTxtCenterStrip = {}
    # Data file name
    fnameTxT = "CRTpositionsSiPM-V8.txt"
    # Let's loop on the file, 2 SiPms at the time
    with open(fnameTxT, 'r') as sample:
        for i in xrange(1168):
            couple = next_n_lines(sample, 2)
            sipmEven  = couple[0].split()
            sipmOdd   = couple[1].split()
        
            eFebAndSiPM  = sipmEven[0]
            eFEB         = eFebAndSiPM[:-2]
            eSiPM        = eFebAndSiPM[-2:]
            eX           = float(sipmEven[1]) 
            eY           = float(sipmEven[2]) 
            eZ           = float(sipmEven[3]) 
            ePanel       = sipmEven[4]
            eLayer       = sipmEven[5]
            eDirection   = sipmEven[6]

            oFebAndSiPM  = sipmOdd[0]
            oFEB         = oFebAndSiPM[:-2]
            oSiPM        = oFebAndSiPM[-2:]
            oX           = float(sipmOdd[1]) 
            oY           = float(sipmOdd[2]) 
            oZ           = float(sipmOdd[3]) 
            oPanel       = int(sipmOdd[4])
            oLayer       = int(sipmOdd[5])
            oDirection   = int(sipmOdd[6])

            if eFEB != oFEB:
                raise ValueError('The SiPMs are not on the same FEB')
    
            # Calculate the strip number
            numOSip = float(oSiPM)
            numESip = float(eSiPM)
            meanSiPM = (numOSip+numESip)/4.
            strip = int(meanSiPM)
            uniquekey = 100*int(eFEB)+strip

            # approximate the center of the strip
            centerPosX = (eX + oX)/2.
            centerPosY = (eY + oY)/2.
            centerPosZ = (eZ + oZ)/2.

            # move it in the right place
            if eFEB in bottom_Modules or eFEB in top_Modules:
                if oDirection == 0:
                    centerPosZ += (signDict[eFEB]*febLenght(eFEB)/2.)
                if oDirection == 1:
                    centerPosX += (signDict[eFEB]*febLenght(eFEB)/2.)
            if eFEB in ft_Modules or eFEB in pipe_Modules:
                if oDirection == 1:
                    centerPosZ += (signDict[eFEB]*febLenght(eFEB)/2.)
                if oDirection == 0:
                    centerPosY += (signDict[eFEB]*febLenght(eFEB)/2.)

            center = [centerPosX, centerPosY, centerPosZ]
            dictionaryDataTxtCenterStrip[uniquekey] = center
        
    return dictionaryDataTxtCenterStrip


#main
def makeStrips():
    alP = open("defineStripsDimensions.txt", "a")

    fnameGdml = "gdml/CRTTxt/p3.txt"
    with open(fnameGdml, 'r') as f:
    
        name = "\"Module"
        for line in f.readlines():
            if  name in line:
                words     = line.split("\"")
                AlTop = words[0]+"\""+words[1]+"\""+words[2]+"\""+words[3]+"_10\""+words[4]+"\""+words[5]+"\""+words[6]+"\""+words[7]+"\""+words[8]+"\""+words[9]+"\""+words[10]
                AlBot = words[0]+"\""+words[1]+"\""+words[2]+"\""+words[3]+"_01\""+words[4]+"\""+words[5]+"\""+words[6]+"\""+words[7]+"\""+words[8]+"\""+words[9]+"\""+words[10]

                alP.write(AlTop)
                alP.write(AlBot)

            else:
                alP.write(line)


#main
def makeStripsMaterial():
    alP = open("defineAlMaterial.txt", "a")
    tag_v = ["10","01"]

    for feb in xrange(73):
        for x in xrange(16):
            for tag in tag_v:
                line1 = "      <volume name=\"volModule_"+ str(feb) +"_strip_"+ str(x) +"_"+ tag + "\">\n"
                line2 = "       <materialref ref=\"ALUMINUM_Al\"/>\n"
                line3 = "       <solidref ref=\"Module_"+ str(feb) +"_strip_"+ str(x) +"_"+ tag +"\"/>\n"
                line5 = "      </volume>\n"
                thisline = line1+line2+line3+line5
                alP.write(thisline)




# main


top_Modules   = ["105" ,"106" ,"107","108" ,"109" ,"111" , "112" ,"113" , "114", "115" ,
                 "116" ,"117" ,"118","119" ,"120" ,"121" , "123" ,"124" , "125", "126" ,
                 "127" ,"128" ,"129","195"]
bottom_Modules = ["11" , "12" , "14","17"  ,"18"  , "19" ,  "22" , "23" ,  "24"]
ft_Modules     = ["26" , "27" , "28", "29" , "30" , "31" ,  "52" , "56" ,  "57" , "58" , "59" , "60" , "61"]
pipe_Modules   = ["15" , "16" , "20", "21" , "46" , "47" ,  "48" , "49" ,  "50" , "51" , 
                  "53" , "54" , "55", "32" , "33" , "34" ,  "35" , "36" ,  "37" , "38" , 
                  "39" , "40" , "41", "42" , "43" , "44" , "45" ]
allMods = top_Modules+bottom_Modules+ft_Modules+pipe_Modules

# This dictionary contains all the centers calculated from the txt file used in data
txtDataCenters    = calculateTxtCenters()
scintDictionary = {}
topAlDictionary = {}
bottomAlDictionary = {}
for m in allMods:
    for x in xrange(16):
        key           = int(m)*100+x
        centers       = txtDataCenters[key]
        centersTop    = centers
        centersBottom = centers

        centersTop[2]    = centersTop[2]+1.1
        centersBottom[2] = centersBottom[2]-1.1

        scintBlockOfText  = prepareBlock(str(key), centers      , 0)
        topBlockOfText    = prepareBlock(str(key), centersTop   , 1)
        bottomBlockOfText = prepareBlock(str(key), centersBottom,-1)


        blockOrder = scintBlockOfText[1]*100 + x 
        scintDictionary   [ blockOrder ] = scintBlockOfText[0]
        topAlDictionary   [ blockOrder ] = topBlockOfText[0]
        bottomAlDictionary[ blockOrder ] = bottomBlockOfText[0]


scintDictOd  = collections.OrderedDict(sorted(scintDictionary.items()))
topDictOd    = collections.OrderedDict(sorted(topAlDictionary.items()))
bottomDictOd = collections.OrderedDict(sorted(bottomAlDictionary.items()))


f = open("scintillationPosition.txt", "a")
for k, v in scintDictOd.items():
    f.write(v)


alP = open("alluminumPosition.txt", "a")
for k, v in topDictOd.items():
    alP.write(v)
for k, v in bottomDictOd.items():
    alP.write(v)


makeStrips()
makeStripsMaterial()
