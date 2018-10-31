from ROOT import *
import os
import math
import argparse
import numpy as np
from array import array




def histoBoundary( histo ):
    if histo.Integral():
        histo.Scale(1./histo.Integral())
    else:
        return 0., 0.,
    # Find average bin content
    content = []
    for i in xrange(1,histo.GetSize() - 1 ):
        if  histo.GetBinContent(i):
            content.append(histo.GetBinContent(i))
    avgContent = float( sum(content) ) / float( len(content) )

    # Find the min and max bins that are above 0.3 of the average
    # I need this to get rid of accidental outsider hits at the boundaries
    binBoundaries = []
    for i in xrange(1,histo.GetSize() - 1 ):
        if  histo.GetBinContent(i) > 0.5*avgContent :
            binBoundaries.append(i)
    
    # Return those bin positions
    #print histo.GetBinCenter(min(binBoundaries)), histo.GetBinCenter(max(binBoundaries))
    
    return histo.GetBinCenter(min(binBoundaries)), histo.GetBinCenter(max(binBoundaries))



def compareHistos(hData, hMC):
    #hData.Rebin(8)
    #hMC.Rebin(8)
    if hData.Integral() and hMC.Integral():
        hData.Sumw2()
        hMC  .Sumw2()
        hData.Scale(1./hData.Integral())
        hMC  .Scale(1./hMC  .Integral())
    else:
        return 0., 0.


    boundariesData =  histoBoundary(hData)
    boundariesMC   =  histoBoundary(hMC)
    #print


#    raw_input()      
    return boundariesData[0] - boundariesMC[0], boundariesData[1] - boundariesMC[1]



def threeInOne(febName):
    # Get the right histos
    fileNameData = "hitPositionPerModule_Data.root"
    fileNameMC   = "cosmics_corsika_cmc_hist_CRTOnly_100Evts.root"

    inFileData   = TFile.Open(fileNameData)
    inFileMC     = TFile.Open(fileNameMC)

    moduleName = "Module_"+ febName 
    hDataX = inFileData.Get("crt/hHitX_" + moduleName)
    hMCX   = inFileMC  .Get("crt/hHitX_" + moduleName)
    hDataY = inFileData.Get("crt/hHitY_" + moduleName)
    hMCY   = inFileMC  .Get("crt/hHitY_" + moduleName)
    hDataZ = inFileData.Get("crt/hHitZ_" + moduleName)
    hMCZ   = inFileMC  .Get("crt/hHitZ_" + moduleName)

    # Cosmetics
    hDataX.SetLineColor(kBlack)
    hMCX  .SetLineColor(kBlue)
    hDataX.SetLineWidth(2)
    hMCX  .SetLineWidth(2)

    hDataY.SetLineColor(kBlack)
    hMCY  .SetLineColor(kBlue)
    hDataY.SetLineWidth(2)
    hMCY  .SetLineWidth(2)

    hDataZ.SetLineColor(kBlack)
    hMCZ  .SetLineColor(kBlue)
    hDataZ.SetLineWidth(2)
    hMCZ  .SetLineWidth(2)


    # Draw histograms
    legend = TLegend(.54,.52,.84,.70)
    legend.AddEntry(hDataX ,"Data")
    legend.AddEntry(hMCX   ,"MC")


    c = TCanvas("c","c",1800,600);
    c.Divide(3,1)
    p1 = c.cd(1)
    p1.SetGrid()
    hMCX  .Draw("histo")
    hDataX.Draw("histoSame")
    legend.Draw("same")

    p2 = c.cd(2)
    p2.SetGrid()
    hMCY  .Draw("histo")
    hDataY.Draw("histoSame")
    legend.Draw("same")

    p3 = c.cd(3)
    p3.SetGrid()
    hMCZ  .Draw("histo")
    hDataZ.Draw("histoSame")
    legend.Draw("same")

    
    
    compareHistosResultsX = compareHistos(hDataX, hMCX)
    compareHistosResultsY = compareHistos(hDataY, hMCY)
    compareHistosResultsZ = compareHistos(hDataZ, hMCZ)
    print  moduleName,  compareHistosResultsX, compareHistosResultsY, compareHistosResultsZ
    raw_input()




parser = argparse.ArgumentParser()
parser.add_argument("febName"     , nargs='?', default = "11", type = str, help="insert febName")
args     = parser.parse_args()
febName = args.febName

threeInOne(febName)


raw_input()  

