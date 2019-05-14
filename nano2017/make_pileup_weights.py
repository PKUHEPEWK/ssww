import ROOT

fout = ROOT.TFile("PileupWeights2016.root","RECREATE")
fdata = ROOT.TFile("PileupData2016Observed.root","READ")
fdataminbiasxsecup = ROOT.TFile("PileupData2016ObservedMinBiasXsecUp.root","READ")

data_hist = fdata.Get("pileup")
data_up_hist = fdataminbiasxsecup.Get("pileup")

mc_hist=ROOT.TH1D("mc","mc",70,0,70)

mc_hist.Sumw2()
data_hist.Sumw2()
data_up_hist.Sumw2()

tchain = ROOT.TChain("Events")
tchain.Add("pileup.root")

#tchain.Add("/afs/cern.ch/work/a/amlevin/data/WGToLNuG_01J_5f_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/E6F2574C-D766-E811-B047-0CC47ABB518A.root")

tchain.Draw("Pileup_nPU >> mc")

fout.cd()

mc_cloned = mc_hist.Clone("mc")
data_cloned = data_hist.Clone("data")
data_up_cloned = data_up_hist.Clone("data_up")

data_cloned.Write()
data_up_cloned.Write()

ratio = data_hist.Clone("ratio")
ratio_up = data_up_hist.Clone("ratio_up")

mc_cloned.Scale(1/mc_cloned.Integral())
ratio.Scale(1/ratio.Integral())
ratio_up.Scale(1/ratio_up.Integral())

ratio.Divide(mc_cloned)
ratio_up.Divide(mc_cloned)

ratio.Write()
ratio_up.Write()
mc_cloned.Write()
