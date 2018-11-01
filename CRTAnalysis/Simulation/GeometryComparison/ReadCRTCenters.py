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



wantedFEB = "14"

def next_n_lines(file_opened, N):
    return [x.strip() for x in islice(file_opened, N)]


top_Modules   = ["105" ,"106" ,"107","108" ,"109" ,"111" , "112" ,"113" , "114", "115" ,
                 "116" ,"117" ,"118","119" ,"120" ,"121" , "123" ,"124" , "125", "126" ,
                 "127" ,"128" ,"129","195"]
bottom_Modules = ["11" , "12" , "14","17"  ,"18"  , "19" ,  "22" , "23" ,  "24"]
ft_Modules     = ["26" , "27" , "28", "29" , "30" , "31" ,  "52" , "56" ,  "57" , "58" , "59" , "60" , "61"]
pipe_Modules   = ["15" , "16" , "20", "21" , "46" , "47" ,  "48" , "49" ,  "50" , "51" , 
                  "53" , "54" , "55", "32" , "33" , "34" ,  "35" , "36" ,  "37" , "38" , 
                  "39" , "40" , "41", "42" , "43" , "44" , "45" ]


hTop      = TH2D("hTop"      , "hTop;    Z; X" ,  125, -300., 1300, 125, -300., 500.)
hBottom   = TH2D("hBottom"   , "hBottom; Z; X" ,  125, -300., 1300, 125, -300., 500.)
hRedCheck = TH2D("hRedCheck" , "hBottom; Z; X" ,  125, -300., 1300, 125, -300., 500.)
hPipe     = TH2D("hPipe"     , "hPipe;   Z; Y" ,  125, -300., 1300, 125, -300., 300.)
hFT       = TH2D("hFT"       , "hFT;     Z; Y" ,  125, -300., 1300, 125, -300., 300.)


hSimTop      = TH2D("hSimTop"      , "hSimTop;    Z; X" ,  125, -300., 1300, 125, -300., 500.)
hSimBottom   = TH2D("hSimBottom"   , "hSimBottom; Z; X" ,  125, -300., 1300, 125, -300., 500.)
hSimPipe     = TH2D("hSimPipe"     , "hSimPipe;   Z; Y" ,  125, -300., 1300, 125, -300., 300.)
hSimFT       = TH2D("hSimFT"       , "hSimFT;     Z; Y" ,  125, -300., 1300, 125, -300., 300.)


allMods = top_Modules+bottom_Modules+ft_Modules+pipe_Modules
#print len(allMods)

striplength = [ 346.0, 346.0, 346.0, 259.6, 259.6, 259.6, 259.6, 227.0, 227.0, 346.0,
                346.0, 346.0, 346.0, 346.0, 346.0, 346.0, 403.8, 403.8, 403.8, 403.8,                    
                403.8, 403.8, 259.6, 259.6, 259.6, 259.6, 259.6, 259.6, 259.6, 259.6,                                                                 
                259.6, 259.6, 259.6, 259.6, 259.6, 259.6, 396.2, 396.2, 396.2, 227.0,                                                              
                227.0, 227.0, 227.0, 227.0, 227.0, 227.0, 227.0, 227.0, 227.0, 360.0,                                                               
                360.0, 360.0, 360.0, 360.0, 360.0, 360.0, 180.0, 180.0, 180.0, 180.0,                                                           
                180.0, 180.0, 365.0, 365.0, 365.0, 365.0, 365.0, 365.0, 180.0, 180.0,                                 
                365.0, 365.0, 365.0]


mod2feb = [ 24,23,22,17,14,18,19,12,11,52,
            31,29,28,27,26,30,61,59,57,60,
            58,56,32,38,36,35,34,33,37,45,
            44,43,42,41,40,39,55,54,53,51,
            49,47,21,16,50,48,46,20,15,107,
            106,105,109,108,112,111,195,123,124,126,
            125,129,115,114,113,116,119,120,127,128,
            117,121,118]




plusFEBs  = [ 119, 120, 121, 109, 105, 106, 107, 125, 126, 128, 129, 119, 120, 121,
               14,  17,  11,  12,  52,  31,  29,  28,  27,  26,  30,  39,  40,  41, 
               42,  43,  44,  45 ]


minusFEBs = [ 113, 114, 115, 116, 117, 118, 127, 195, 123, 124, 108, 112, 111,  22,
               23,  24,  19,  18,  60,  61,  58,  59,  56,  57,  37,  33,  34,  32, 
               35,  36,  38,  53,  54,  55,  15,  16,  20,  21,  46,  47,  48,  49, 
               50,  51]




'''
# A bunch of checks I hopefully don't need anymore
found = False
#for p in itertools.chain(pipe_Modules,top_Modules,ft_Modules,bottom_Modules):
for p in itertools.chain(minusFEBs,plusFEBs):
    for m in mod2feb:
        if str(m) == str(p):
            found = True
    if not found:
        print "-----------------", p
    found = False

print len(mod2feb), len(striplength)
import collections
print [item for item, count in collections.Counter(mod2feb).items() if count > 1]
'''


lengthsDict = {}
for i in xrange(0,73):
    lengthsDict[str(mod2feb[i])] = striplength[i]


print "THIS LENGHT IS WRONG!!! FEB11 ", striplength[11] 
print "THIS LENGHT IS WRONG!!! FEB12 ", striplength[12] 

signDict = {}
for i in plusFEBs:
    signDict[str(i)] = 1.
for i in minusFEBs:
    signDict[str(i)] = -1.

#pprint.pprint( lengthsDict )
#print len(lengthsDict)


'''
Panel Map ==>
- 0: bottom
- 1: ft
- 2: pipe
- 3: top
'''

fnameTxT = "CRTpositionsSiPM-V8.txt"
dictionaryDataTxtCenterStrip = {}

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
                centerPosZ += (signDict[eFEB]*lengthsDict[eFEB]/2.)
            if oDirection == 1:
                centerPosX += (signDict[eFEB]*lengthsDict[eFEB]/2.)
        if eFEB in ft_Modules or eFEB in pipe_Modules:
            if oDirection == 1:
                centerPosZ += (signDict[eFEB]*lengthsDict[eFEB]/2.)
            if oDirection == 0:
                centerPosY += (signDict[eFEB]*lengthsDict[eFEB]/2.)


        if eFEB in bottom_Modules:
            hBottom.Fill(centerPosZ,centerPosX)

        if eFEB in top_Modules:
            hTop.Fill(centerPosZ,centerPosX)

        if eFEB in pipe_Modules:
            hPipe.Fill(centerPosZ,centerPosY)

        if eFEB in ft_Modules:
            hFT.Fill(centerPosZ,centerPosY)

        center = [centerPosX, centerPosY, centerPosZ]
        dictionaryDataTxtCenterStrip[uniquekey] = center
        



fnameGdml = "gdml_CRT_B_bars_volumePlacement_file.gdml"
dictionaryMCGdmlCenterStrip = {}

with open(fnameGdml, 'r') as f:
    for line in f.readlines():
        if "position" not in line:
            continue
        else:
            w  = line.split("\"")
            FEB   = mod2feb[int((w[1].split("_"))[1])]
            strip = int((w[1].split("_"))[3])
            uniquekey = 100*FEB+strip 
            centerPosX = float( w[5]) + 130.
            centerPosY = float( w[7]) 
            centerPosZ = float( w[9]) + 520.

            center = [centerPosX, centerPosY, centerPosZ]
            dictionaryMCGdmlCenterStrip[uniquekey] = center

            if str(FEB) in bottom_Modules:
                hSimBottom.Fill(centerPosZ,centerPosX)

            if str(FEB) in top_Modules:
                hSimTop.Fill(centerPosZ,centerPosX)

            if str(FEB) in ft_Modules:
                hSimFT.Fill(centerPosZ,centerPosY)

            if str(FEB) in pipe_Modules:
                hSimPipe.Fill(centerPosZ,centerPosY)

inverted = 0
dictionaryDifferences        = {}
dictionaryDifferences_orig   = {}
dictionaryDifferences_invert = {}
for feb in mod2feb:
    sqSum_orig   = 0
    sqSum_invert = 0

    for x in xrange(16):
        key         = feb*100+x
        invertedkey = feb*100 + (15-x)
        dataPosition      = dictionaryDataTxtCenterStrip[key]
        simPosition_orig    = dictionaryMCGdmlCenterStrip[key]
        simPosition_invert  = dictionaryMCGdmlCenterStrip[invertedkey]

        diff_orig    = [dataPosition[0] - simPosition_orig[0]  , dataPosition[1] - simPosition_orig[1]  , dataPosition[2] - simPosition_orig[2] ]
        diff_invert  = [dataPosition[0] - simPosition_invert[0], dataPosition[1] - simPosition_invert[1], dataPosition[2] - simPosition_invert[2] ]

        sqSum_orig   += ( diff_orig[0]*diff_orig[0]  + diff_orig[1]*diff_orig[1] + diff_orig[2]*diff_orig[2] )
        sqSum_invert += ( diff_invert[0]*diff_invert[0]  + diff_invert[1]*diff_invert[1] + diff_invert[2]*diff_invert[2] )

        dictionaryDifferences[key]   = diff_orig
        dictionaryDifferences_orig[key]   = diff_orig
        dictionaryDifferences_invert[key] = diff_invert

#        if str(feb) == wantedFEB:
#            print key, "%.2f" % diff[0] , "%.2f" % diff[1] , "%.2f" % diff[2]

    if sqSum_invert < sqSum_orig:
        inverted += 1
        print "INVERTED", feb, inverted
        for x in xrange(16):
            key = feb*100 + (15-x)
            dictionaryDifferences[key] = dictionaryDifferences_invert[key] 


#print 
#print len(dictionaryMCGdmlCenterStrip)
pprint.pprint( dictionaryDifferences)   



hRedCheck.SetMarkerStyle(20)
hRedCheck.SetMarkerSize(2)
hRedCheck.SetMarkerColor(kRed)

hBottom.SetMarkerStyle(20)
hTop.SetMarkerStyle(20)
hPipe.SetMarkerStyle(20)
hFT.SetMarkerStyle(20)
hBottom.SetMarkerSize(1)
hTop.SetMarkerSize(1)
hPipe.SetMarkerSize(1)
hFT.SetMarkerSize(1)


hSimBottom.SetMarkerStyle(21)
hSimTop.SetMarkerStyle(21)
hSimPipe.SetMarkerStyle(21)
hSimFT.SetMarkerStyle(21)
hSimBottom.SetMarkerSize(1)
hSimTop.SetMarkerSize(1)
hSimPipe.SetMarkerSize(1)
hSimFT.SetMarkerSize(1)
hSimBottom.SetMarkerColor(kRed)
hSimTop.SetMarkerColor(kRed)
hSimPipe.SetMarkerColor(kRed)
hSimFT.SetMarkerColor(kRed)


fOut = TFile("CenterOut.root","recreate")
fOut.cd()
fOut.Add(hBottom)
fOut.Add(hRedCheck)
fOut.Add(hTop)
fOut.Add(hPipe)
fOut.Add(hFT)

fOut.Add(hSimBottom)
fOut.Add(hSimTop)
fOut.Add(hSimPipe)
fOut.Add(hSimFT)

fOut.Write()
fOut.Close()



raw_input()  

