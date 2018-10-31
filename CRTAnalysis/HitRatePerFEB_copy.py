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

inFile   = TFile.Open(fileName)




print "---------------------- Top --------------------------"
hTopHistos_top_long = []
hTopHistos_top_short = []

top_longModules  = ["105" ,"106" ,"107","108" ,"109" ,"111" , "112" ,"113" , "114", "115" ,"116" ,"117","118" ,"119" ,"120" , "121"]
top_shortModules = ["123" , "124", "125" ,"126" ,"127","128" ,"129" ,"195"]

for l in top_longModules:
    tempHist    = inFile.Get("crt/hEvtRateTop_"+l)
    tempHist.SetLineColor(kRed)
    tempHist.SetLineWidth(2)
    hTopHistos_top_long.append(tempHist)

for s in top_shortModules:
    tempHist    = inFile.Get("crt/hEvtRateTop_"+s)
    tempHist.SetLineColor(kBlue)
    tempHist.SetLineWidth(2)
    hTopHistos_top_short.append(tempHist)

c1 = TCanvas("c1","the fit canvas",600,600);
c1.cd()
mean_top_long = []
mean_top_short = []
print "Top_Long Modules Means:"
for h in hTopHistos_top_long:
    h.GetXaxis().SetRangeUser(0, 20)
    h.GetYaxis().SetRangeUser(0, 1000)
    h.GetYaxis().SetTitleOffset(1.5)
    h.Draw("sames")
    mean = h.GetMean()
    print h.GetTitle(), "---> ", mean
    mean_top_long.append(mean)
    h.SetTitle("Rate for Top Modules; N hits in 4 ms; N events")

print "Average of Means -------------> ", reduce(lambda x, y: x + y, mean_top_long) / len(mean_top_long)

print
print "Top_Short Modules Means:"
for h in hTopHistos_top_short:
    h.Draw("sames")
    mean = h.GetMean()
    print h.GetTitle(), "---> ", mean
    mean_top_short.append(mean)


legendTop = TLegend(.54,.52,.84,.70);
legendTop.AddEntry(hTopHistos_top_short[1]   ,"Top_Short Modules ");
legendTop.AddEntry(hTopHistos_top_long[1]   ,"Top_Long Modules ");
legendTop.Draw("same")
print "Average of Means -------------> ", reduce(lambda x, y: x + y, mean_top_short) / len(mean_top_short)
print "-----------------------------------------------------"

print

print "---------------------- Bottom --------------------------"
hBottomHistos_bottom_long   = []
hBottomHistos_bottom_medium = []
hBottomHistos_bottom_short  = []

bottom_shortModules   = ["11"  , "12" ]
bottom_mediumModules  = ["14" ,"17"  ,"18"  ,"19"  ]
bottom_longModules    = ["22" ,"23"  ,  "24"]


for l in bottom_longModules:
    tempHist    = inFile.Get("crt/hEvtRateBottom_"+l)
    tempHist.SetLineColor(kRed)
    tempHist.SetLineWidth(2)
    hBottomHistos_bottom_long.append(tempHist)

for m in bottom_mediumModules:
    tempHist    = inFile.Get("crt/hEvtRateBottom_"+m)
    tempHist.SetLineColor(kGreen-2)
    tempHist.SetLineWidth(2)
    hBottomHistos_bottom_medium.append(tempHist)

for s in bottom_shortModules:
    tempHist    = inFile.Get("crt/hEvtRateBottom_"+s)
    tempHist.SetLineColor(kBlue)
    tempHist.SetLineWidth(2)
    hBottomHistos_bottom_short.append(tempHist)

cBottom = TCanvas("cBottom","the fit canvas",600,600);
cBottom.cd()
mean_bottom_long   = []
mean_bottom_medium = []
mean_bottom_short  = []
print "Bottom_Long Modules Means:"
for h in hBottomHistos_bottom_long:
    h.GetXaxis().SetRangeUser(0, 20)
    h.GetYaxis().SetRangeUser(0, 1500)
    h.GetYaxis().SetTitleOffset(1.5)
    h.Draw("sames")
    mean = h.GetMean()
    print h.GetTitle(), "---> ", mean
    mean_bottom_long.append(mean)
    h.SetTitle("Rate for Bottom Modules; N hits in 4 ms; N events")
print "Average of Means -------------> ", reduce(lambda x, y: x + y, mean_bottom_long) / len(mean_bottom_long)
print 
for h in hBottomHistos_bottom_medium:
    h.GetXaxis().SetRangeUser(0, 20)
    h.GetYaxis().SetRangeUser(0, 1500)
    h.GetYaxis().SetTitleOffset(1.5)
    h.Draw("sames")
    mean = h.GetMean()
    print h.GetTitle(), "---> ", mean
    mean_bottom_medium.append(mean)

print "Average of Means -------------> ", reduce(lambda x, y: x + y, mean_bottom_medium) / len(mean_bottom_medium)

print
print "Bottom_Short Modules Means:"
for h in hBottomHistos_bottom_short:
    h.Draw("sames")
    mean = h.GetMean()
    print h.GetTitle(), "---> ", mean
    mean_bottom_short.append(mean)


legendBottom = TLegend(.54,.52,.84,.70);
legendBottom.AddEntry(hBottomHistos_bottom_short[1]   ,"Bottom_Short Modules ");
legendBottom.AddEntry(hBottomHistos_bottom_medium[1]   ,"Bottom_Medium Modules ");
legendBottom.AddEntry(hBottomHistos_bottom_long[1]   ,"Bottom_Long Modules ");
legendBottom.Draw("same")
print "Average of Means -------------> ", reduce(lambda x, y: x + y, mean_bottom_short) / len(mean_bottom_short)
print "-----------------------------------------------------"



print

print "---------------------- Pipe --------------------------"
hPipeHistos_pipe_long   = []
hPipeHistos_pipe_medium = []
hPipeHistos_pipe_short  = []

pipe_shortModules   = ["15" , "16" , "20" , "21" , "46" , "47" , "48" , "49" , "50" , "51" ]
pipe_longModules    = ["53" , "54" , "55"]
pipe_mediumModules  = ["32" , "33" , "34" , "35" , "36" , "37" , "38" , "39" , "40" , "41" , "42" , "43" , "44" , "45" ]



for l in pipe_longModules:
    tempHist    = inFile.Get("crt/hEvtRatePipe_"+l)
    tempHist.SetLineColor(kRed)
    tempHist.SetLineWidth(2)
    hPipeHistos_pipe_long.append(tempHist)

for m in pipe_mediumModules:
    tempHist    = inFile.Get("crt/hEvtRatePipe_"+m)
    tempHist.SetLineColor(kGreen-2)
    tempHist.SetLineWidth(2)
    hPipeHistos_pipe_medium.append(tempHist)

for s in pipe_shortModules:
    tempHist    = inFile.Get("crt/hEvtRatePipe_"+s)
    tempHist.SetLineColor(kBlue)
    tempHist.SetLineWidth(2)
    hPipeHistos_pipe_short.append(tempHist)

cPipe = TCanvas("cPipe","the fit canvas",600,600);
cPipe.cd()
mean_pipe_long   = []
mean_pipe_medium = []
mean_pipe_short  = []
print "Pipe_Long Modules Means:"
for h in hPipeHistos_pipe_long:
    h.GetXaxis().SetRangeUser(0, 20)
    h.GetYaxis().SetRangeUser(0, 1500)
    h.GetYaxis().SetTitleOffset(1.5)
    h.Draw("sames")
    mean = h.GetMean()
    print h.GetTitle(), "---> ", mean
    mean_pipe_long.append(mean)
    h.SetTitle("Rate for Pipe Modules; N hits in 4 ms; N events")
print "Average of Means -------------> ", reduce(lambda x, y: x + y, mean_pipe_long) / len(mean_pipe_long)
print
for h in hPipeHistos_pipe_medium:
    h.GetXaxis().SetRangeUser(0, 20)
    h.GetYaxis().SetRangeUser(0, 1500)
    h.GetYaxis().SetTitleOffset(1.5)
    h.Draw("sames")
    mean = h.GetMean()
    print h.GetTitle(), "---> ", mean
    mean_pipe_medium.append(mean)

print "Average of Means -------------> ", reduce(lambda x, y: x + y, mean_pipe_medium) / len(mean_pipe_medium)

print
print "Pipe_Short Modules Means:"
for h in hPipeHistos_pipe_short:
    h.Draw("sames")
    mean = h.GetMean()
    print h.GetTitle(), "---> ", mean
    mean_pipe_short.append(mean)


legendPipe = TLegend(.54,.52,.84,.70);
legendPipe.AddEntry(hPipeHistos_pipe_short[1]   ,"Pipe_Short Modules ");
legendPipe.AddEntry(hPipeHistos_pipe_medium[1]   ,"Pipe_Medium Modules ");
legendPipe.AddEntry(hPipeHistos_pipe_long[1]   ,"Pipe_Long Modules ");
legendPipe.Draw("same")
print "Average of Means -------------> ", reduce(lambda x, y: x + y, mean_pipe_short) / len(mean_pipe_short)
print "-----------------------------------------------------"





ft_shortModules     = ["26" , "27" , "28" , "29" , "30" , "31" , "52" ]
ft_longModules      = ["56" , "57" , "58" , "59" , "60" , "61"]






'''
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
'''

raw_input()  

