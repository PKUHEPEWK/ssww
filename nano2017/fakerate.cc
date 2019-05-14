#include <ROOT/RDF/HistoModels.hxx>

using namespace ROOT;  // RDataFrame's namespace

void fakerate() {
    string channel = "muon";
    TChain chain("Events");
    string path = ".";
    string trigger;
    string pid;
    if (channel == "muon") {
        chain.Add("/home/pku/xiaoj/nano_2016/MuonEG_Run2016C.root");
        trigger = "HLT_Mu17_TrkIsoVVL";
        pid     = "13";
    }
    else if (channel == "electron") {
        chain.Add("electron*.root");
        trigger = "(HLT_Ele12_CaloIdL_TrackIdL_IsoVL_PFJet30 || HLT_Ele17_CaloIdL_TrackIdL_IsoVL_PFJet30 || HLT_Ele23_CaloIdL_TrackIdL_IsoVL_PFJet30)";
        pid     = "11";
    }

    RDataFrame d(chain);

    //string fake_cut = trigger + " && n_fakeable_leptons == 1 && met < 30 && mt < 20";
    //string true_cut = trigger + "&& n_tight_leptons == 1 && met < 30 && mt < 20";
    string fake_cut = trigger + " && lepton_fakeable[0] && lepton_pdg_id[1]<0 && lepton_pdg_id[0]==" + pid + " && met < 30 && mt < 20";
    string true_cut = trigger + " && lepton_tight[0] && lepton_pdg_id[1]<0 &&lepton_pdg_id[0]== " + pid + " && met < 30 && mt < 20";

    //auto fake_cut = [](double x) { return (HLT_Mu17_TrkIsoVVL && n_fakeable_leptons == 1 && met < 30 && mt < 20); };
    //auto true_cut = [](double x) { return (HLT_Mu17_TrkIsoVVL && n_tight_leptons == 1 && met < 30 && mt < 20); };
    double etabin[] = {0., 0.5, 1., 1.479, 2., 2.5};
    double ptbin[]  = {20, 25, 30, 35};

    auto fake_template = d.Filter(fake_cut)
                             .Define("eta_tmp", "abs(lepton_eta[0]);")
                             .Define("pt_tmp", "if(lepton_pt[0]>35) return 32.5; else return (double)lepton_pt[0];")
                             .Histo2D({"fake", "fake;|#eta|;p_{T}", 5, etabin, 3, ptbin}, "eta_tmp", "pt_tmp");
    fake_template->Sumw2();

    auto true_template = d.Filter(true_cut)
                             .Define("eta_tmp", "abs(lepton_eta[0]);")
                             .Define("pt_tmp", "if(lepton_pt[0]>35) return 32.5; else return (double)lepton_pt[0];")
                             .Histo2D({"true", "true;|#eta|;p_{T}", 5, etabin, 3, ptbin}, "eta_tmp", "pt_tmp");
    true_template->Sumw2();
    // for GetPtr() follow: https://root-forum.cern.ch/t/tlegend-addentry-no-known-conversion-from-root-rresultptr-tgraph-to-const-tobject/30873
    true_template->Divide(fake_template.GetPtr());
    TCanvas c1("c1", "c1", 1200, 900);
    true_template->Draw("colztext");
    c1.Print("fakerate.pdf");
}
