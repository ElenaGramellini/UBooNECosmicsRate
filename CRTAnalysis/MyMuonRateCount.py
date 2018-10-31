from ROOT import *
import os
import math
import argparse
import numpy as np
from array import array


# python loop over floats
def frange(start, stop, step):
    x = start
    while x < stop:
        yield x
        x += step


###################################################################
########     Take file name from the command line   ###############
######## The default is HighlandFormula_histo.root  ###############
###################################################################
parser = argparse.ArgumentParser()
parser.add_argument("fileName"     , nargs='?', default = "track_tree_EXTBNB.root", type = str, help="insert fileName")
args     = parser.parse_args()
fileName = args.fileName


###################################################################
####################       Get TTree       ########################
###################################################################
inFile   = TFile.Open(fileName)
#tTree    = inFile.Get("crt/CRTMuonRate")
tTree    = inFile.Get("crt/CRTMuonRate")

hPEBottom  = TH1D("hPEBottom" , "hPEBottom"  , 3000, 0., 3000 )
hPETop     = TH1D("hPETop"    , "hPETop"     , 3000, 0., 3000 )
hHitBottom = TH1D("hHitBottom", "n Hit Bottom; N_{hit} per evt;Counts" ,  500, 0., 1000  )
hHitTop    = TH1D("hHitTop"   , "n Hit Top   ; N_{hit} per evt;Counts" ,  500, 0., 1000  )
    
hHitTimeDiffBottom = TH1D("hHitTimeDiffBottom"   , "#Delta t Bottom;#Delta t_{consecutive hits} [ns]; Counts"  ,  300, 0., 300  )
hHitTimeDiffTop    = TH1D("hHitTimeDiffTop"      , "#Delta t Top; #Delta t_{consecutive hits} [ns]; Counts"    ,  300, 0., 300  )


hTimeVsXVsZ_Bottom  = TH3D("hTimeVsXVsX_Bottom"   , "timeVsXVsX_Bottom" ,  260, -100., 1200, 180, -300., 600,  600, -2000000, 4000000 )
hTimeVsXVsZ_Top     = TH3D("hTimeVsXVsX_Top"      , "timeVsXVsX_Top"    ,  260, -100., 1200, 180, -300., 600,  600, -2000000, 4000000 )

speed_of_light = 0.299792 #m/ns


print "Entries: ", tTree.GetEntry()
sillyCount =0 
for entry in tTree:
     sillyCount += 1
     if not sillyCount % 10000:
          print sillyCount
#     if sillyCount == 100:
#         break
     # Get the important variables from the ttree
     nCRThits    = entry.nCRThits   
     hit_plane   = entry.hit_plane
     hit_time_s  = entry.hit_time_s
     hit_charge  = entry.hit_charge
     hit_time0   = entry.hit_time0
     hit_posx    = entry.hit_posx
     hit_posy    = entry.hit_posy
     hit_posz    = entry.hit_posz


     timeSortedBottom_Hits = []
     timeSortedTop_Hits    = []
     
     for i in xrange(nCRThits):
         if hit_plane[i] == 1:
             continue

         if hit_plane[i] == 2:
             continue

         if hit_plane[i] == 0:
             hPEBottom.Fill(hit_charge[i])
             timeSortedBottom_Hits.append(hit_time0[i])
             hTimeVsXVsZ_Bottom.Fill(hit_posz[i], hit_posx[i], hit_time0[i])
             #print hit_plane[i], hit_posz[i], hit_posx[i], hit_time0[i]

         if hit_plane[i] == 3:
             hPETop.Fill(hit_charge[i])
             timeSortedTop_Hits.append(hit_time0[i])
             hTimeVsXVsZ_Top.Fill(hit_posz[i], hit_posx[i], hit_time0[i])
             #print hit_plane[i], hit_posz[i], hit_posx[i], hit_time0[i]

     timeSortedBottom_Hits.sort()
     timeSortedTop_Hits.sort()

#     print timeSortedBottom_Hits 
#     print timeSortedTop_Hits 

     for i in xrange(1,len(timeSortedBottom_Hits)):
         hHitTimeDiffBottom.Fill(timeSortedBottom_Hits[i] - timeSortedBottom_Hits[i-1])

     for i in xrange(1,len(timeSortedTop_Hits)):
         hHitTimeDiffTop.Fill(timeSortedTop_Hits[i] - timeSortedTop_Hits[i-1])

     hHitBottom .Fill(len(timeSortedBottom_Hits))
     hHitTop    .Fill(len(timeSortedTop_Hits))

#     break


# Save everything
outFile = TFile("CRT_Muon_Rate.root","recreate")
outFile.cd()
hPEBottom.Write()
hHitBottom.Write()
hPETop.Write()
hHitTop.Write()
hHitTimeDiffBottom.Write()
hHitTimeDiffTop.Write()
hTimeVsXVsZ_Bottom.Write()
hTimeVsXVsZ_Top.Write()
outFile.Write()
outFile.Close()


raw_input()  

