/// \file
/// \ingroup tutorial_fit
/// \notebook -js
/// Get in memory an histogram from a root file and fit a user defined function.
/// Note that a user defined function must always be defined
/// as in this example:
///  - first parameter: array of variables (in this example only 1-dimension)
///  - second parameter: array of parameters
/// Note also that in case of user defined functions, one must set
/// an initial value for each parameter.
///
/// \macro_image
/// \macro_output
/// \macro_code
///
/// \author Rene Brun


#include "TCanvas.h"
#include "TRandom3.h"
#include "TH1.h"
#include "TF1.h"
#include "TFile.h"
#include "TROOT.h"
#include "TStyle.h"
#include "TMath.h"

Double_t
poissonf(Double_t*x,Double_t*par)                                         
{                                                                              
  return par[0]*TMath::Poisson(x[0],par[1]);
}    

void myfit()
{
  gStyle->SetOptFit(1111);

  TFile *hsimpleFile = TFile::Open("CRT_Muon_Rate.root");
  //TFile *hsimpleFile = TFile::Open("HitsAtSameTime.root");
  //TFile *hsimpleFile = TFile::Open("NearFar.root");
  if (!hsimpleFile) return;
  
  TCanvas *c1 = new TCanvas("c1","the fit canvas",500,400);
  
  TH1F *hHitBottom = (TH1F*)hsimpleFile->Get("hHitBottom");
  TH1F *hHitTop = (TH1F*)hsimpleFile->Get("hHitTop");


  // Creates a Root function based on function fitf above
  TF1 *func    = new TF1("pois",poissonf,0,30,2); //30
  TF1 *funcTop = new TF1("pois",poissonf,1,150,2); //150

  // Sets initial values and parameter names
  func->SetParameters(1,1);
  // Fit histogram in range defined by function
  hHitBottom->Fit(func,"r");
  func->Draw("same");
  std::cout<<"Bottom "<<func->GetParameter(1)<<"\n";
  

  
  TCanvas *c2 = new TCanvas("c2","the fit canvas",500,400);
  c2->cd();
  funcTop->SetParameters(1000,60);
  hHitTop->Fit(funcTop,"r");
  funcTop->Draw("same");
  std::cout<<"Top "<<func->GetParameter(0)<<"\n";
  


  // Gets integral of function between fit limits
  printf("Integral of function = %g\n",func->Integral(0,30));
}
