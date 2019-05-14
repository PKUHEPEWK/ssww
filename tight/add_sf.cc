#include "TBranch.h"
#include "TFile.h"
#include "TH1D.h"
#include "TH2D.h"
#include "TTree.h"

void add_sf() {
    double xs = 0.2;

    TFile* f            = TFile::Open("outfakelepton_MUON.root");
    TFile* f_pu_weights = TFile::Open("PileupWeights2016.root.root");

    TH1D* nWeightedEvents = (TH1D*)f->Get("nWeightedEvents");

    TFile* electron_id_sf_file = TFile::Open("egammaEffi.txt_EGM2D.root.electron.id");
    TH2D*  electron_id_sf      = (TH2D*)electron_id_sf_file->Get("EGamma_SF2D");

    TFile* electron_reco_sf_file = TFile::Open("egammaEffi.txt_EGM2D.root.electron.reco");
    TH2D*  electron_reco_sf      = (TH2D*)electron_reco_sf_file->Get("EGamma_SF2D");

    TFile* muon_iso_sf_file = TFile::Open("EfficienciesAndSF_GH.root.iso");
    TH2D*  muon_iso_sf      = (TH2D*)muon_iso_sf_file->Get("TightISO_TightID_pt_eta/abseta_pt_ratio");

    TFile* muon_id_sf_file = TFile::Open("EfficienciesAndSF_GH.root.id");
    TH2D*  muon_id_sf      = (TH2D*)muon_id_sf_file->Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio");

    TFile f("tree3.root", "update");

    double id_sf[9] = {0};
    double pu_weight;
    double xs_sf;

    TTree*   t           = (TTree*)f->Get("Events");
    TBranch* b_id_sf     = t->Branch("id_sf", id_sf, "id_sf[9]/D");
    TBranch* b_pu_weight = t->Branch("pu_weight", &pu_weight, "pu_weight/D");
    TBranch* b_xs_sf     = t->Branch("xs_sf", &xs_sf, "xs_sf/D");

    Long64_t nentries = t->GetEntries();  // read the number of entries in the t

    int    lepton_pdg_id[9];
    double lepton_pt[9];
    double lepton_eta[9];

    t->SetBranchAddress("lepton_pdg_id", lepton_pdg_id);
    t->SetBranchAddress("lepton_pt", lepton_pt);
    t->SetBranchAddress("lepton_eta", lepton_eta);

    for (Long64_t i = 0; i < nentries; i++) {
        for (int j = 0; j < 9; j++) {
            if (abs(lepton_pdg_id[i]) == 11) {
                id_sf[i] = electron_id_sf->GetBinContent(electron_id_sf->GetXaxis()->FindFixBin(lepton_eta[i]), electron_id_sf->GetYaxis()->FindFixBin(lepton_pt[i]));
                id_sf[i] *= electron_reco_sf->GetBinContent(electron_reco_sf->GetXaxis()->FindFixBin(lepton_eta[i]), 1);
            }
            else if (abs(lepton_pdg_ids[i]) == 13) {
                id_sf[i] = muon_iso_sf->GetBinContent(muon_iso_sf->GetXaxis()->FindFixBin(abs(lepton_eta[i])), muon_iso_sf->GetYaxis()->FindFixBin(min(lepton_pt[i], muon_iso_sf->GetYaxis()->GetBinCenter(muon_id_sf->GetNbinsY()))));
                id_sf[i] *= muon_id_sf->GetBinContent(muon_id_sf->GetXaxis()->FindFixBin(abs(lepton_eta[i])), muon_id_sf->GetYaxis()->FindFixBin(min(lepton_pt[i], muon_id_sf->GetYaxis()->GetBinCenter(muon_id_sf->GetNbinsY()))));
            }
            else
                id_sf[i] = 99.0;
        }
        pu_weight = 1;
        xs_sf     = xs * 1000 / nWeightedEvents->GetBinContent(1);
        b_id_sf->Fill();
        b_pu_weight->Fill();
        b_xs_sf->Fill();
    }
    t->Write("", TObject::kOverwrite);  // save only the new version of the tree
}
