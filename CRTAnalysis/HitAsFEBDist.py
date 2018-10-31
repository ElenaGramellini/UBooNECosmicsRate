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

#gStyle.SetOptStat(0)
inFile   = TFile.Open(fileName)


print "---------------------- Top --------------------------"
hTopHistos   = []
top_Modules  = ["105" ,"106" ,"107","108" ,"109" ,"111" , "112" ,"113" , "114", "115" ,"116" ,"117","118" ,"119" ,"120" , "121","123" , "124", "125" ,"126" ,"127","128" ,"129" ,"195"]

h125    = inFile.Get("crt/hEvtRateTop_125")
h126    = inFile.Get("crt/hEvtRateTop_126")
h112    = inFile.Get("crt/hEvtRateTop_112")
h111    = inFile.Get("crt/hEvtRateTop_111")


hFar  = h125.Clone("FarEnd")
hNear = h126.Clone("NearEnd")
hFar .Add(h112)
hNear.Add(h111)

hNear.SetLineWidth(2)
hFar.SetLineWidth(2)

hNear.SetLineColor(kBlue)
hFar.SetLineColor(kRed)

c1 = TCanvas("c1","the fit canvas",600,600);
c1.cd()
hFar.Draw("")
hNear.Draw("sames")

hFar.SetTitle("Near-Far FEB halves comparison 419, 420, 421; N hits per 4 [ms]; Count")



h105    = inFile.Get("crt/hEvtRateTop_105")
h109    = inFile.Get("crt/hEvtRateTop_109")
h122    = inFile.Get("crt/hEvtRateTop_195")
h123    = inFile.Get("crt/hEvtRateTop_123")


hFar2  = h123.Clone("FarEnd2")
hNear2 = h122.Clone("NearEnd2")
hFar2 .Add(h105)
hNear2.Add(h109)

hNear2.SetLineWidth(2)
hFar2.SetLineWidth(2)

hNear2.SetLineColor(kBlue)
hFar2.SetLineColor(kRed)

c1 = TCanvas("c1","the fit canvas",600,600);
c1.cd()
hFar2.Draw("")
hNear2.Draw("sames")
hFar2.SetTitle("Near-Far FEB halves comparison 413, 414, 415; N hits per 4 [ms]; Count")



outFile = TFile("NearFar.root","recreate")
hFar.Write()
hNear.Write()
outFile.Write()
outFile.Close()


raw_input()  





