#include "TH1D.h"
#include "TH2D.h"
#include "TTree.h"
#include <Riostream.h>
#include <algorithm>
#include <sstream>

using namespace ROOT;  // RDataFrame's namespace
using namespace std;

void exe(string filename, double xs);
void addweight() {
    ifstream in("xs_list_2016.txt");
    string   line;
    string   filename;
    string   xs_str;
    double   xs;
    if (in) {
        while (getline(in, line)) {
            stringstream sline(line);
            sline >> filename;
            sline >> xs_str;
            xs = atof(xs_str.c_str());
            exe(filename, xs);
        }
    }
}
void exe(string filename, double xs) {
    // puweight
    TFile* f_pu        = TFile::Open("PileupWeights2016.root");
    TH1D*  h_pu_weight = (TH1D*)f_pu->Get("ratio");
    int    n_lepton    = 2;
    double id_sf[2]    = {1., 1.};

    //TFile* f = TFile::Open("tree_1.root", "update");

    TFile* f = TFile::Open(("../" + filename).c_str(), "update");
    cout << "DouDou:   " << filename << endl;
    double nevents;
    TH1D*  nWeightedEvents;
    if (xs > 0) {
        nWeightedEvents = (TH1D*)f->Get("nWeightedEvents");
        nevents         = nWeightedEvents->GetBinContent(1);
    }
    // electron
    // -- tight id
    TFile* electron_tight_id_sf_file = TFile::Open("2016LegacyReReco_ElectronTight_Fall17V2.root");
    TH2D*  electron_tight_id_sf      = (TH2D*)electron_tight_id_sf_file->Get("EGamma_SF2D");
    // -- veto id
    TFile* electron_loose_id_sf_file = TFile::Open("2016_ElectronWPVeto_Fall17V2.root");
    TH2D*  electron_loose_id_sf      = (TH2D*)electron_loose_id_sf_file->Get("EGamma_SF2D");
    // -- reco sf
    TFile* electron_reco_sf_file = TFile::Open("egammaEffi.txt_EGM2D.root.electron.reco");
    TH2D*  electron_reco_sf      = (TH2D*)electron_reco_sf_file->Get("EGamma_SF2D");
    // muon
    // -- iso
    TFile* muon_iso_sf_file_bf = TFile::Open("EfficienciesAndSF_BCDEF_ISO.root");
    TFile* muon_iso_sf_file_gh = TFile::Open("EfficienciesAndSF_GH_ISO.root");
    // --- tight iso
    TH2D* muon_tight_iso_sf_bf = (TH2D*)muon_iso_sf_file_bf->Get("TightISO_TightID_pt_eta/abseta_pt_ratio");
    TH2D* muon_tight_iso_sf_gh = (TH2D*)muon_iso_sf_file_gh->Get("TightISO_TightID_pt_eta/abseta_pt_ratio");
    // -- very loose iso, in fact I use loose iso, because I didn't find the very loose iso sf
    TH2D* muon_loose_iso_sf_bf = (TH2D*)muon_iso_sf_file_bf->Get("LooseISO_TightID_pt_eta/abseta_pt_ratio");
    TH2D* muon_loose_iso_sf_gh = (TH2D*)muon_iso_sf_file_gh->Get("LooseISO_TightID_pt_eta/abseta_pt_ratio");

    // -- id
    TFile* muon_id_sf_file_bf = TFile::Open("EfficienciesAndSF_BCDEF_ID.root");
    TFile* muon_id_sf_file_gh = TFile::Open("EfficienciesAndSF_GH_ID.root");
    // --- tight id
    TH2D* muon_tight_id_sf_bf = (TH2D*)muon_id_sf_file_bf->Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio");
    TH2D* muon_tight_id_sf_gh = (TH2D*)muon_id_sf_file_gh->Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio");
    // --- loose id
    TH2D* muon_loose_id_sf_bf = (TH2D*)muon_id_sf_file_bf->Get("MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio");
    TH2D* muon_loose_id_sf_gh = (TH2D*)muon_id_sf_file_gh->Get("MC_NUM_LooseID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio");
    //https://github.com/PKUHEPEWK/WGamma/blob/master/2016/eff_scale_factor.py

    double   bf               = 0.5497;
    double   gh               = 0.4503;
    double   iso              = 1.;
    double   id               = 1.;
    double   reco             = 1.;
    double   pu_weight        = 1.;
    double   xs_sf            = 1.;
    TTree*   t                = (TTree*)f->Get("Events");
    TBranch* id_sf_branch     = t->Branch("id_sf", id_sf, "id_sf[2]/D");
    TBranch* pu_weight_branch = t->Branch("pu_weight", &pu_weight, "pu_weight/D");
    TBranch* xs_sf_branch     = t->Branch("xs_sf", &xs_sf, "xs_sf/D");
    Long64_t nentries         = t->GetEntries();  // read the number of entries in the t3

    float lepton_pt[n_lepton];
    float lepton_eta[n_lepton];
    int   lepton_pdg_id[n_lepton];
    char  lepton_tight[n_lepton];
    char  lepton_fakeable[n_lepton];
    int   npu;
    float ntruepu;
    float gen_weight;

    t->SetBranchAddress("lepton_pt", lepton_pt);
    t->SetBranchAddress("lepton_eta", lepton_eta);
    t->SetBranchAddress("lepton_pdg_id", lepton_pdg_id);
    t->SetBranchAddress("lepton_tight", lepton_tight);
    t->SetBranchAddress("lepton_fakeable", lepton_fakeable);
    t->SetBranchAddress("npu", &npu);
    t->SetBranchAddress("ntruepu", &ntruepu);
    t->SetBranchAddress("gen_weight", &gen_weight);

    for (Long64_t n = 0; n < nentries; n++) {
        if (n % 10000000 == 100) {
            //break;
            std::cout << "entry:" << n << std::endl;
        }
        t->GetEntry(n);
        // xs sf
        if (xs < 0.) {
            xs_sf     = 1.;
            pu_weight = 1.;
        }
        else {
            if (gen_weight < 0)
                xs_sf = -1. * xs * 1000 * 35.9 / nevents;
            else
                xs_sf = xs * 1000 * 35.9 / nevents;
            // pu weight
            pu_weight = h_pu_weight->GetBinContent(h_pu_weight->GetXaxis()->FindBin(npu));
            // id sf
            for (int i = 0; i < n_lepton; i++) {
                iso  = 1.;
                id   = 1.;
                reco = 1.;
                if (abs(lepton_pdg_id[i]) == 11) {
                    if (lepton_tight[i]) {
                        id       = electron_tight_id_sf->GetBinContent(electron_tight_id_sf->GetXaxis()->FindFixBin(lepton_eta[i]), electron_tight_id_sf->GetYaxis()->FindFixBin(lepton_pt[i]));
                        reco     = electron_reco_sf->GetBinContent(electron_reco_sf->GetXaxis()->FindFixBin(lepton_eta[i]), 1);
                        id_sf[i] = id * reco;
                    }
                    else if (lepton_fakeable[i]) {
                        //id       = electron_loose_id_sf->GetBinContent(electron_loose_id_sf->GetXaxis()->FindFixBin(lepton_eta[i]), electron_loose_id_sf->GetYaxis()->FindFixBin(lepton_pt[i]));
                        reco     = electron_reco_sf->GetBinContent(electron_reco_sf->GetXaxis()->FindFixBin(lepton_eta[i]), 1);
                        id_sf[i] = id * reco;
                    }
                    else {
                        id       = electron_loose_id_sf->GetBinContent(electron_loose_id_sf->GetXaxis()->FindFixBin(lepton_eta[i]), electron_loose_id_sf->GetYaxis()->FindFixBin(lepton_pt[i]));
                        reco     = electron_reco_sf->GetBinContent(electron_reco_sf->GetXaxis()->FindFixBin(lepton_eta[i]), 1);
                        id_sf[i] = id * reco;
                    }
                }
                else if (abs(lepton_pdg_id[i]) == 13) {
                    if (lepton_tight[i]) {
                        id       = bf * muon_tight_id_sf_bf->GetBinContent(muon_tight_id_sf_bf->GetXaxis()->FindFixBin(abs(lepton_eta[i])), muon_tight_id_sf_bf->GetYaxis()->FindFixBin(min((double)lepton_pt[i], muon_tight_id_sf_bf->GetYaxis()->GetBinCenter(muon_tight_id_sf_bf->GetNbinsY())))) + gh * muon_tight_id_sf_gh->GetBinContent(muon_tight_id_sf_gh->GetXaxis()->FindFixBin(abs(lepton_eta[i])), muon_tight_id_sf_gh->GetYaxis()->FindFixBin(min((double)lepton_pt[i], muon_tight_id_sf_gh->GetYaxis()->GetBinCenter(muon_tight_id_sf_gh->GetNbinsY()))));
                        iso      = bf * muon_tight_iso_sf_bf->GetBinContent(muon_tight_iso_sf_bf->GetXaxis()->FindFixBin(abs(lepton_eta[i])), muon_tight_iso_sf_bf->GetYaxis()->FindFixBin(min((double)lepton_pt[i], muon_tight_iso_sf_bf->GetYaxis()->GetBinCenter(muon_tight_iso_sf_bf->GetNbinsY())))) + gh * muon_tight_iso_sf_gh->GetBinContent(muon_tight_iso_sf_gh->GetXaxis()->FindFixBin(abs(lepton_eta[i])), muon_tight_iso_sf_gh->GetYaxis()->FindFixBin(min((double)lepton_pt[i], muon_tight_iso_sf_gh->GetYaxis()->GetBinCenter(muon_tight_iso_sf_gh->GetNbinsY()))));
                        id_sf[i] = id * iso;
                    }
                    else if (lepton_fakeable[i]) {
                        id       = bf * muon_tight_id_sf_bf->GetBinContent(muon_tight_id_sf_bf->GetXaxis()->FindFixBin(abs(lepton_eta[i])), muon_tight_id_sf_bf->GetYaxis()->FindFixBin(min((double)lepton_pt[i], muon_tight_id_sf_bf->GetYaxis()->GetBinCenter(muon_tight_id_sf_bf->GetNbinsY())))) + gh * muon_tight_id_sf_gh->GetBinContent(muon_tight_id_sf_gh->GetXaxis()->FindFixBin(abs(lepton_eta[i])), muon_tight_id_sf_gh->GetYaxis()->FindFixBin(min((double)lepton_pt[i], muon_tight_id_sf_gh->GetYaxis()->GetBinCenter(muon_tight_id_sf_gh->GetNbinsY()))));
                        iso      = bf * muon_loose_iso_sf_bf->GetBinContent(muon_loose_iso_sf_bf->GetXaxis()->FindFixBin(abs(lepton_eta[i])), muon_loose_iso_sf_bf->GetYaxis()->FindFixBin(min((double)lepton_pt[i], muon_loose_iso_sf_bf->GetYaxis()->GetBinCenter(muon_loose_iso_sf_bf->GetNbinsY())))) + gh * muon_loose_iso_sf_gh->GetBinContent(muon_loose_iso_sf_gh->GetXaxis()->FindFixBin(abs(lepton_eta[i])), muon_loose_iso_sf_gh->GetYaxis()->FindFixBin(min((double)lepton_pt[i], muon_loose_iso_sf_gh->GetYaxis()->GetBinCenter(muon_loose_iso_sf_gh->GetNbinsY()))));
                        id_sf[i] = id * iso;
                    }
                    else {
                        id       = bf * muon_loose_id_sf_bf->GetBinContent(muon_loose_id_sf_bf->GetXaxis()->FindFixBin(abs(lepton_eta[i])), muon_loose_id_sf_bf->GetYaxis()->FindFixBin(min((double)lepton_pt[i], muon_loose_id_sf_bf->GetYaxis()->GetBinCenter(muon_loose_id_sf_bf->GetNbinsY())))) + gh * muon_loose_id_sf_gh->GetBinContent(muon_loose_id_sf_gh->GetXaxis()->FindFixBin(abs(lepton_eta[i])), muon_loose_id_sf_gh->GetYaxis()->FindFixBin(min((double)lepton_pt[i], muon_loose_id_sf_gh->GetYaxis()->GetBinCenter(muon_loose_id_sf_gh->GetNbinsY()))));
                        id_sf[i] = id * iso;
                    }
                }
            }
        }
        id_sf_branch->Fill();
        pu_weight_branch->Fill();
        xs_sf_branch->Fill();
    }
    f->cd();
    t->Write("", TObject::kOverwrite);  // save only the new version of the tree
    // 1st, delete TH
    /*
    delete h_pu_weight;
    delete electron_tight_id_sf;
    delete electron_loose_id_sf;
    delete electron_reco_sf;
    delete muon_tight_iso_sf_bf;
    delete muon_tight_iso_sf_gh;
    delete muon_loose_iso_sf_bf;
    delete muon_loose_iso_sf_gh;
    delete muon_tight_id_sf_bf;
    delete muon_tight_id_sf_gh;
    delete muon_loose_id_sf_bf;
    delete muon_loose_id_sf_gh;
    delete nWeightedEvents;

    delete t;
    // 2nd, delete TFile
    delete muon_id_sf_file_gh;
    delete muon_id_sf_file_bf;
    delete muon_iso_sf_file_gh;
    delete muon_iso_sf_file_bf;
    delete electron_loose_id_sf_file;
    delete electron_tight_id_sf_file;
    delete muon_iso_sf_file_gh;
    delete muon_iso_sf_file_gh;
    delete muon_iso_sf_file_gh;
    delete f_pu;
    delete f;
    */
}
