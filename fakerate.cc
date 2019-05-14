#include "TH1D.h"
#include "TH2D.h"
#include "TTree.h"
#include <Riostream.h>
#include <sstream>

using namespace ROOT;  // RDataFrame's namespace
using namespace std;

void fakerate() {
    string channel = "muon";
    string pid;
    TChain chain("Events");
    if (channel == "muon") {
        pid = "13";
        chain.Add("DoubleMuon_*.root");
    }
    else if (channel == "electron") {
        pid = "11";
        chain.Add("DoubleEG_*.root");
    }
    // cut template
    /*
    auto cut_fakeable = [](int _num, double _pt, double _met, double _met_phi, double _lepton_phi, int _pid) {
        if (n_fakeable_leptons == 1) {
            double mt_tmp = lepton_pt[3] * met * (1 - cos(met_phi - lepton_phi[3]));
            if (abs(lepton_pdg_id[3]) == 13 && mt_tmp < 20 && met < 30)
                return true;
            else
                return false;
        }
        else
            return false;
    };
    */
    string cut_fakeable = "if (n_tight_leptons==0 && n_fakeable_leptons == 1) {double mt_tmp = lepton_pt[3] * met * (1 - cos(met_phi - lepton_phi[3]));if (abs(lepton_pdg_id[3]) == " + pid + " && mt_tmp < 20 && met < 30) return true; else {return false;}} else {return false;};";
    string cut_tight    = "if (n_tight_leptons == 1) {double mt_tmp = lepton_pt[0] * met * (1 - cos(met_phi - lepton_phi[3]));if (abs(lepton_pdg_id[0]) == " + pid + " && mt_tmp < 20 && met < 30) return true; else {return false;}} else {return false;};";

    RDataFrame d(chain);
    auto       fakeable = d.Filter(cut_fakeable);
    auto       tight    = d.Filter(cut_tight);
    auto       h_fake   = fakeable.Histo2D({"count", "count_fakeable:|#eta|:pt", 5u, 0., 2.5, 3u, 20., 35.}, "abs(lepton_eta[3])", "lepton_pt[3]");
    auto       h_tight  = tight.Histo2D({"count", "count_fakeable:|#eta|:pt", 5u, 0., 2.5, 3u, 20., 35.}, "abs(lepton_eta[3])", "lepton_pt[3]");
    h_fake->sumW2();
    h_tight->sumW2();
    auto h_ratio = h_tight
}

sqrt(2 * (leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[1]][0].p4()).Pt() * event.MET_pt * (1 - cos(event.MET_phi - (leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[1]][0].p4()).Phi())))
