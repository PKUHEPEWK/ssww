#include "TH1D.h"
#include "TH2D.h"
#include "TTree.h"
#include <Riostream.h>
#include <sstream>

using namespace ROOT;  // RDataFrame's namespace
using namespace std;

string double_to_str(double val) {
    stringstream ss;
    ss << val;
    return ss.str();
}
void add_scale_factor() {
    double xs        = 0.001;
    double pu_weight = 3.;

    TFile* f = TFile::Open("outfakelepton_MUON.root");

    TH1D* nWeightedEvents = (TH1D*)f->Get("nWeightedEvents");

    TFile* electron_id_sf_file = TFile::Open("egammaEffi.txt_EGM2D.root.electron.id");
    TH2D*  electron_id_sf      = (TH2D*)electron_id_sf_file->Get("EGamma_SF2D");

    TFile* electron_reco_sf_file = TFile::Open("egammaEffi.txt_EGM2D.root.electron.reco");
    TH2D*  electron_reco_sf      = (TH2D*)electron_reco_sf_file->Get("EGamma_SF2D");

    TFile* muon_iso_sf_file = TFile::Open("EfficienciesAndSF_GH.root.iso");
    TH2D*  muon_iso_sf      = (TH2D*)muon_iso_sf_file->Get("TightISO_TightID_pt_eta/abseta_pt_ratio");

    TFile* muon_id_sf_file = TFile::Open("EfficienciesAndSF_GH.root.id");
    TH2D*  muon_id_sf      = (TH2D*)muon_id_sf_file->Get("MC_NUM_TightID_DEN_genTracks_PAR_pt_eta/abseta_pt_ratio");

    using doubles = RVec<double>;
    using ints    = RVec<int>;
    //https://github.com/PKUHEPEWK/WGamma/blob/master/2016/eff_scale_factor.py
    auto cut = [](ints& lepton_pdg_ids, doubles& lepton_pts, doubles& lepton_etas) {
        auto id_sfs = lepton_pts;
        for (int i = 0; i < 9; i++) {
            if (abs(lepton_pdg_ids[i]) == 11) {
                id_sfs[i] = electron_id_sf->GetBinContent(electron_id_sf->GetXaxis()->FindFixBin(lepton_etas[i]), electron_id_sf->GetYaxis()->FindFixBin(lepton_pts[i]));
                id_sfs[i] *= electron_reco_sf->GetBinContent(electron_reco_sf->GetXaxis()->FindFixBin(lepton_etas[i]), 1);
            }
            else if (abs(lepton_pdg_ids[i]) == 13) {
                id_sfs[i] = muon_iso_sf->GetBinContent(muon_iso_sf->GetXaxis()->FindFixBin(abs(lepton_etas[i])), muon_iso_sf->GetYaxis()->FindFixBin(min(lepton_pts[i], muon_iso_sf->GetYaxis()->GetBinCenter(muon_id_sf->GetNbinsY()))));
                id_sfs[i] *= muon_id_sf->GetBinContent(muon_id_sf->GetXaxis()->FindFixBin(abs(lepton_etas[i])), muon_id_sf->GetYaxis()->FindFixBin(min(lepton_pts[i], muon_id_sf->GetYaxis()->GetBinCenter(muon_id_sf->GetNbinsY()))));
            }
            else
                id_sfs[i] = 99.0;
        }
        return id_sfs;
    }

    RDataFrame d("Events", f);

    auto d_with_columns = d.Define("id_sf", cut, {"lepton_pdg_id", "lepton_pt", "lepton_eta"})
                              .Define("puweight", double_to_str(pu_weight))
                              .Define("xs_sf", double_to_str(xs));
    d_with_columns.Snapshot("Events", "output.root");
}
