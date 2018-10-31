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
parser.add_argument("fileName"     , nargs='?', default = "RateAndDeltaT.root", type = str, help="insert fileName")
args     = parser.parse_args()
fileName = args.fileName

gStyle.SetOptStat(0)
inFile   = TFile.Open(fileName)


botDeltaT    = inFile.Get("crt/HitDeltaTBot")
topDeltaT    = inFile.Get("crt/HitDeltaTTop")
pipeDeltaT   = inFile.Get("crt/HitDeltaTPipe")
ftDeltaT     = inFile.Get("crt/HitDeltaTFT")
botDeltaT.SetLineColor(kBlue)
topDeltaT.SetLineColor(kRed)
pipeDeltaT.SetLineColor(kGreen-2)
ftDeltaT.SetLineColor(kYellow-2)

cT = TCanvas("cT","the fit canvas",1200,600);
cT.Divide(2,1)
p1 = cT.cd(1)
p1.SetLogy()
botDeltaT.SetTitle("Delta t consecutive hits on Bottom; #Delta t consecutive [ns]; Count")
botDeltaT.Draw()
p2 = cT.cd(2)
p2.SetLogy()
topDeltaT.Draw()
topDeltaT.SetTitle("Delta t consecutive hits on Top; #Delta t consecutive [ns]; Count")

cT1 = TCanvas("cT1","the fit canvas",1200,600);
cT1.Divide(2,1)
p1 = cT1.cd(1)
p1.SetLogy()
ftDeltaT.SetTitle("Delta t consecutive hits on FT; #Delta t consecutive [ns]; Count")
ftDeltaT.Draw()
p2 = cT1.cd(2)
p2.SetLogy()
pipeDeltaT.Draw()
pipeDeltaT.SetTitle("Delta t consecutive hits on Pipe; #Delta t consecutive [ns]; Count")


print "---------------------- Top --------------------------"
hTopHistos   = []
top_Modules  = ["105" ,"106" ,"107","108" ,"109" ,"111" , "112" ,"113" , "114", "115" ,"116" ,"117","118" ,"119" ,"120" , "121","123" , "124", "125" ,"126" ,"127","128" ,"129" ,"195"]

for l in top_Modules:
    tempHist    = inFile.Get("crt/hDeltaTTop_"+l)
    tempHist.SetLineColor(kRed)
    tempHist.SetLineWidth(2)
    hTopHistos.append(tempHist)


c1 = TCanvas("c1","the fit canvas",600,600);
c1.cd()
c1.SetLogy()
print "Top_Long Modules Means:"
for h in hTopHistos:
    h.GetXaxis().SetRangeUser(0, 100000)
    #h.GetYaxis().SetRangeUser(0, 1000)
    #h.GetYaxis().SetTitleOffset(1.5)
    h.Draw("sames")
    h.SetTitle("Delta t consecutive hits on same FEB -- All top FEB; #Delta t consecutive [ns]; Count")




print "---------------------- Bottom --------------------------"
hBottomHistos   = []
bottom_Modules  = ["11"  , "12" , "14" ,"17"  ,"18"  ,"19" , "22" ,"23"  ,  "24"]

for l in bottom_Modules:
    tempHist    = inFile.Get("crt/hDeltaTBottom_"+l)
    tempHist.SetLineColor(kBlue)
    tempHist.SetLineWidth(2)
    hBottomHistos.append(tempHist)


c1 = TCanvas("c1","the fit canvas",600,600);
c1.cd()
c1.SetLogy()
print "Bottom_Long Modules Means:"
for h in hBottomHistos:
    h.GetXaxis().SetRangeUser(0, 100000)
    #h.GetYaxis().SetRangeUser(0, 1000)
    #h.GetYaxis().SetTitleOffset(1.5)
    h.Draw("sames")
    h.SetTitle("Delta t consecutive hits on same FEB -- All bottom FEB; #Delta t consecutive [ns]; Count")


print "---------------------- FT --------------------------"
hFTHistos   = []
ft_Modules  = ["26" , "27" , "28" , "29" , "30" , "31" , "52" , "56" , "57" , "58" , "59" , "60" , "61"]

for l in ft_Modules:
    tempHist    = inFile.Get("crt/hDeltaTFT_"+l)
    tempHist.SetLineColor(kYellow-2)
    tempHist.SetLineWidth(2)
    hFTHistos.append(tempHist)


c1f = TCanvas("c1f","the fit canvas",600,600);
c1f.cd()
c1f.SetLogy()
print "FT_Long Modules Means:"
for h in hFTHistos:
    h.GetXaxis().SetRangeUser(0, 100000)
    #h.GetYaxis().SetRangeUser(0, 1000)
    #h.GetYaxis().SetTitleOffset(1.5)
    h.Draw("sames")
    h.SetTitle("Delta t consecutive hits on same FEB -- All FT FEB; #Delta t consecutive [ns]; Count")


print "---------------------- Pipe --------------------------"
hPipeHistos   = []
pipe_Modules  = ["15" , "16" , "20" , "21" , "46" , "47" , "48" , "49" , "50" , "51" , "53" , "54" , "55" , "32" , "33" , "34" , "35" , "36" , "37" , "38" , "39" , "40" , "41" , "42" , "43" , "44" , "45" ]

for l in pipe_Modules:
    tempHist    = inFile.Get("crt/hDeltaTPipe_"+l)
    tempHist.SetLineColor(kGreen-2)
    tempHist.SetLineWidth(2)
    hPipeHistos.append(tempHist)


c1p = TCanvas("c1p","the fit canvas",600,600);
c1p.cd()
c1p.SetLogy()
print "Pipe_Long Modules Means:"
for h in hPipeHistos:
    h.GetXaxis().SetRangeUser(0, 100000)
    #h.GetYaxis().SetRangeUser(0, 1000)
    #h.GetYaxis().SetTitleOffset(1.5)
    h.Draw("sames")
    h.SetTitle("Delta t consecutive hits on same FEB -- All Pipe FEB; #Delta t consecutive [ns]; Count")



raw_input()  





