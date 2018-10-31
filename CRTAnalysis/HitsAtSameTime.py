from ROOT import *
import os
import math
import argparse
import numpy as np
import copy
from array import array



class crtHitSimple:
     def __init__(self, x, y, z, t, ch):
         self.x  = x
         self.y  = y
         self.z  = z
         self.t  = t
         self.ch = ch


def hitDistance( hit1, hit2 ):
    distance = (hit1.x - hit2.x)*(hit1.x - hit2.x) + (hit1.y - hit2.y)*(hit1.y - hit2.y) + (hit1.z - hit2.z)*(hit1.z - hit2.z)  
    distance = math.sqrt(distance)
    return distance


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
#tTree    = inFile.Get("crt/trackdump")
tTree    = inFile.Get("crt/CRTMuonRate")



    
hHitTimeDiffBottom = TH1D("hHitTimeDiffBottom"   , "hHitTimeDiffBottom" ,  1000, 0., 1000  )
hHitTimeDiffTop    = TH1D("hHitTimeDiffTop"      , "hHitTimeDiffTop"    ,  1000, 0., 1000  )

hHitTimeDiffBottomVsDist = TH2D("hHitTimeDiffBottomVsDist","#Delta Time Vs Dist hit -- Bottom; #Delta t_{consecutive hits} [ns]; Dist_{consecutive hits} [cm] " ,  300, 0., 300, 500, 0, 500  )
hHitTimeDiffTopVsDist    = TH2D("hHitTimeDiffTopVsDist"   ,"#Delta Time Vs Dist hit -- Top; #Delta t_{consecutive hits} [ns]; Dist_{consecutive hits} [cm] " ,  300, 0., 300, 500, 0, 500  )

hBlobBottom  = TH2D("hBlobBottomXVsZ_Bottom"   , "hBlobXVsZ_Bottom; Z; X" ,  125, -150., 1150, 125, -150., 500.)
hBlobBottomY = TH3D("hBlobBottomXVsZ_BottomY"  , "hBlobXVsZ_Bottom; Z; X" ,  125, -150., 1150, 125, -150., 500., 100,-200,-300)
hBlobTop     = TH2D("hBlobTopXVsZ_Top"   , "hBlobXVsZ_Top; Z; X" ,  125, -300., 1300, 125, -300., 500.)

hBlobTop10_20 = TH2D("hBlobTop10_20"   , "hBlobXVsZ_Top 10_20; Z; X" ,  125, -300., 1300, 125, -300., 500.)
hBlobTop30_40 = TH2D("hBlobTop30_40"   , "hBlobXVsZ_Top 30_40; Z; X" ,  125, -300., 1300, 125, -300., 500.)
hBlobTop50_60 = TH2D("hBlobTop50_60"   , "hBlobXVsZ_Top 50_60; Z; X" ,  125, -300., 1300, 125, -300., 500.)
hBlobTop70_80 = TH2D("hBlobTop70_80"   , "hBlobXVsZ_Top 70_80; Z; X" ,  125, -300., 1300, 125, -300., 500.)


hPEBottom  = TH1D("hPEBottom" , "hPEBottom"  , 3000, 0., 3000 )
hPETop     = TH1D("hPETop"    , "hPETop"     , 3000, 0., 3000 )
hHitBottom = TH1D("hHitBottom", "n Hit Bottom; N_{hit} per evt;Counts" ,  500, 0., 1000  )
hHitTop    = TH1D("hHitTop"   , "n Hit Top   ; N_{hit} per evt;Counts" ,  500, 0., 1000  )

hTime    = TH1D("hTime"      , "time"    ,  700, -2500000, 4500000 )

hOverlap  = TH2D("hOverlap"   , "Overlap; Z; X", 6, 600, 630, 40, -150, 250)

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


     hitTimesBottom        = []
     timeSortedBottom_Hits = []

     hitTimesTop           = []
     timeSortedTop_Hits    = []

     if nCRThits == 0:
          continue

     for i in xrange(nCRThits):
         if hit_plane[i] == 1:
             continue

         if hit_plane[i] == 2:
             continue

         if hit_plane[i] == 0:
              thisHit = crtHitSimple(hit_posx[i], hit_posy[i],hit_posz[i],hit_time0[i], hit_charge[i]) 
              hitTimesBottom.append(hit_time0[i])
              timeSortedBottom_Hits.append(thisHit)

         if hit_plane[i] == 3:
              thisHit = crtHitSimple(hit_posx[i], hit_posy[i],hit_posz[i],hit_time0[i], hit_charge[i]) 
              hitTimesTop.append(hit_time0[i])
              timeSortedTop_Hits.append(thisHit)


     # Order the hits in time
     if len(hitTimesBottom) != 0:
          hitTimesBottom, timeSortedBottom_Hits  = (list(t) for t in  zip(*sorted(zip(hitTimesBottom, timeSortedBottom_Hits))))

     if len(hitTimesTop) != 0:
          hitTimesTop   , timeSortedTop_Hits     = (list(t) for t in  zip(*sorted(zip(hitTimesTop   , timeSortedTop_Hits   ))))

     
     hitsOverlapBottom = []
     # Remove duplicates hits and fill histograms -- Bottom
     i = 1
     while i < len(timeSortedBottom_Hits):
          timeDiff  = hitTimesBottom[i] - hitTimesBottom[i-1]
          spaceDist = hitDistance(timeSortedBottom_Hits[i], timeSortedBottom_Hits[i-1])   
          if (timeDiff < 2 and  spaceDist < 1):
               timeSortedBottom_Hits.pop(i-1)
          else:
               hTime.Fill(timeSortedBottom_Hits[i-1].t)
               hHitTimeDiffBottom.Fill(timeDiff)
               hHitTimeDiffBottomVsDist.Fill(timeDiff,spaceDist)
               hOverlap.Fill(timeSortedBottom_Hits[i-1].z,timeSortedBottom_Hits[i-1].x)
               if timeSortedBottom_Hits[i-1].z < 630 and timeSortedBottom_Hits[i-1].z > 600 and timeSortedBottom_Hits[i-1].x < 50 and timeSortedBottom_Hits[i-1].x > -150:
                    hitsOverlapBottom.append(timeSortedBottom_Hits[i-1])

               if i+1 == len(timeSortedBottom_Hits):
                    hTime.Fill(timeSortedBottom_Hits[i-1].t)
                    hOverlap.Fill(timeSortedBottom_Hits[i].z,timeSortedBottom_Hits[i].x)
                    if timeSortedBottom_Hits[i].z < 630 and timeSortedBottom_Hits[i].z > 600 and timeSortedBottom_Hits[i].x < 50 and timeSortedBottom_Hits[i].x > -150:
                         hitsOverlapBottom.append(timeSortedBottom_Hits[i])

               if (timeDiff < 6 and spaceDist > 10 and spaceDist < 25):
                    hBlobBottom.Fill((timeSortedBottom_Hits[i-1].z),(timeSortedBottom_Hits[i-1].x))
                    hBlobBottomY.Fill((timeSortedBottom_Hits[i-1].z) ,(timeSortedBottom_Hits[i-1].x),(timeSortedBottom_Hits[i-1].y))
                    if i+1 == len(timeSortedBottom_Hits):
                         hBlobBottom.Fill((timeSortedBottom_Hits[i].z),(timeSortedBottom_Hits[i].x))
                         hBlobBottomY.Fill((timeSortedBottom_Hits[i].z) ,(timeSortedBottom_Hits[i].x),(timeSortedBottom_Hits[i].y))
               i += 1


     # Remove duplicates hits and fill histograms -- Top
     i = 1
     while i < len(timeSortedTop_Hits):
          timeDiff  = hitTimesTop[i] - hitTimesTop[i-1]
          spaceDist = hitDistance(timeSortedTop_Hits[i], timeSortedTop_Hits[i-1])   
          if (timeDiff < 2 and  spaceDist < 1):
               timeSortedTop_Hits.pop(i-1)
          else:
               hHitTimeDiffTop.Fill(timeDiff)
               hHitTimeDiffTopVsDist.Fill(timeDiff,spaceDist)
               if timeDiff < 3 and spaceDist > 10 and spaceDist < 20:
                    hBlobTop.Fill((timeSortedTop_Hits[i-1].z),(timeSortedTop_Hits[i-1].x))
                    hBlobTop10_20.Fill((timeSortedTop_Hits[i-1].z),(timeSortedTop_Hits[i-1].x))
               if timeDiff < 3 and spaceDist > 30 and spaceDist < 40:
                    hBlobTop.Fill((timeSortedTop_Hits[i-1].z),(timeSortedTop_Hits[i-1].x))
                    hBlobTop30_40.Fill((timeSortedTop_Hits[i-1].z),(timeSortedTop_Hits[i-1].x))
               if timeDiff < 3 and spaceDist > 50 and spaceDist < 60:
                    hBlobTop.Fill((timeSortedTop_Hits[i-1].z),(timeSortedTop_Hits[i-1].x))
                    hBlobTop50_60.Fill((timeSortedTop_Hits[i-1].z),(timeSortedTop_Hits[i-1].x))
               if timeDiff < 3 and spaceDist > 70 and spaceDist < 80:
                    hBlobTop.Fill((timeSortedTop_Hits[i-1].z),(timeSortedTop_Hits[i-1].x))
                    hBlobTop70_80.Fill((timeSortedTop_Hits[i-1].z),(timeSortedTop_Hits[i-1].x))

               if i+1 == len(timeSortedBottom_Hits):
                    if timeDiff < 3 and spaceDist > 10 and spaceDist < 20:
                         hBlobTop.Fill((timeSortedTop_Hits[i].z),(timeSortedTop_Hits[i].x))
                         hBlobTop10_20.Fill((timeSortedTop_Hits[i].z),(timeSortedTop_Hits[i].x))
                    if timeDiff < 3 and spaceDist > 30 and spaceDist < 40:
                         hBlobTop.Fill((timeSortedTop_Hits[i].z),(timeSortedTop_Hits[i].x))
                         hBlobTop30_40.Fill((timeSortedTop_Hits[i].z),(timeSortedTop_Hits[i].x))
                    if timeDiff < 3 and spaceDist > 50 and spaceDist < 60:
                         hBlobTop.Fill((timeSortedTop_Hits[i].z),(timeSortedTop_Hits[i].x))
                         hBlobTop50_60.Fill((timeSortedTop_Hits[i].z),(timeSortedTop_Hits[i].x))
                    if timeDiff < 3 and spaceDist > 70 and spaceDist < 80:
                         hBlobTop.Fill((timeSortedTop_Hits[i].z),(timeSortedTop_Hits[i].x))
                         hBlobTop70_80.Fill((timeSortedTop_Hits[i].z),(timeSortedTop_Hits[i].x))
               
               i += 1

     hHitBottom .Fill(len(timeSortedBottom_Hits))
     hHitTop    .Fill(len(timeSortedTop_Hits))

# Save everything
outFile = TFile("HitsAtSameTime.root","recreate")
outFile.cd()
hHitTimeDiffBottom.Write()
hHitTimeDiffBottomVsDist.Write()
hBlobBottom.Write()
hBlobTop.Write()
hBlobTop10_20.Write()
hBlobTop30_40.Write()
hBlobTop50_60.Write()
hBlobTop70_80.Write()

hPEBottom.Write()
hHitBottom.Write()
hPETop.Write()
hHitTop.Write()


hTime.Write()
hOverlap.Write()
hHitTimeDiffTop.Write()
hHitTimeDiffTopVsDist.Write()
hBlobBottomY.Write()


outFile.Write()
outFile.Close()


raw_input()  

