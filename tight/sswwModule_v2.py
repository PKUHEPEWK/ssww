import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

leptonsize=9
jetsize=9
#triggersize=32

class sswwProducer(Module):
    def __init__(self,sortkey = lambda x : x.pt,reverse=True,selector=None,maxObjects=None, isData = False):
        self.sortkey = lambda (obj,j,i) : sortkey(obj)
        self.reverse = reverse
        self.selector = [(selector[coll] if coll in selector else (lambda x: True)) for coll in self.input] if selector else None # pass dict([(collection_name,lambda obj : selection(obj)])
        self.maxObjects = maxObjects # save only the first maxObjects objects passing the selection in the merged collection
        self.isData = isData
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("run",  "i");
        self.out.branch("lumi",  "i");
        self.out.branch("event",  "l");
        self.out.branch("npu",  "I");
        self.out.branch("ntruepu",  "F");
        self.out.branch("npvs","I");
        self.out.branch("gen_weight",  "F");

        self.out.branch("loose_tauVeto","B");
        self.out.branch("fakeable_tauVeto","B");
        self.out.branch("tight_tauVeto","B");
        self.out.branch("n_tight_leptons","I");
        self.out.branch("n_fakeable_leptons","I");
        self.out.branch("n_loose_leptons","I");
        self.out.branch("veto_3l_tight","B");
        self.out.branch("veto_3l_fakeable","B");
        self.out.branch("veto_3l_loose","B");
        self.out.branch("veto_wz_tight","B");
        self.out.branch("veto_wz_fakeable","B");
        self.out.branch("veto_wz_loose","B");
        self.out.branch("lepton_idx",  "I", lenVar="leptonsize");
        self.out.branch("lepton_pdg_id",  "I", lenVar="leptonsize");
        self.out.branch("lepton_pt",  "F", lenVar="leptonsize");
        self.out.branch("lepton_eta",  "F", lenVar="leptonsize");
        self.out.branch("lepton_phi",  "F", lenVar="leptonsize");
        self.out.branch("lepton_mass",  "F", lenVar="leptonsize");
        self.out.branch("lepton_real",  "B", lenVar="leptonsize");
        self.out.branch("lepton_mishits",  "I", lenVar="leptonsize");
        self.out.branch("lepton_tkIsoId",  "I", lenVar="leptonsize");
        self.out.branch("mll",  "F", lenVar="leptonsize");

        self.out.branch("bveto","I");
        self.out.branch("n_tight_jets","I");
        self.out.branch("n_fakeable_jets","I");
        self.out.branch("n_loose_jets","I");
        self.out.branch("jet_idx",  "I", lenVar="jetsize");
        self.out.branch("jet_id",  "I", lenVar="jetsize");
        self.out.branch("jet_pt",  "F", lenVar="jetsize");
        self.out.branch("jet_eta",  "F", lenVar="jetsize");
        self.out.branch("jet_phi",  "F", lenVar="jetsize");
        self.out.branch("jet_mass",  "F", lenVar="jetsize");
        self.out.branch("jet_btagCSVV2",  "F", lenVar="jetsize");
        self.out.branch("mjj","F", lenVar="jetsize");

        self.out.branch("met",  "F");
        self.out.branch("met_phi",  "F");
        self.out.branch("mt0",  "F");
        self.out.branch("mt1",  "F");
        self.out.branch("mt2",  "F");
        self.out.branch("puppimet",  "F");
        self.out.branch("puppimet_phi",  "F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""

        if not self.isData:
            if not (event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ or event.HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL or event.HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL or event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ or event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL or event.HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL_DZ or event.HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL or event.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ or event.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL or event.HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL or event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL or event.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL or event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ or event.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ or event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ or event.HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf or event.HLT_IsoMu20 or event.HLT_IsoMu22 or event.HLT_IsoMu24 or event.HLT_IsoMu27 or event.HLT_IsoTkMu20 or event.HLT_IsoTkMu22 or event.HLT_IsoTkMu24 or event.HLT_IsoTkMu27 or event.HLT_Mu45_eta2p1 or event.HLT_Mu50 or event.HLT_Ele25_eta2p1_WPTight_Gsf or event.HLT_Ele27_eta2p1_WPLoose_Gsf or event.HLT_Ele27_WPTight_Gsf or event.HLT_Ele27_WPTight_Gsf or event.HLT_Ele30_WPTight_Gsf or event.HLT_Ele35_WPLoose_Gsf):
                return False
            else:
                pass
        else:
            pass
        # refer to: https://github.com/cms-nanoAOD/nanoAOD-tools/blob/b20be01e2087412051abb5d5b59d0a3d07835207/python/postprocessing/modules/common/collectionMerger.py#L56-L60
        # merge Electron and Muon to Lepton
        input = ["Electron","Muon"]
        coll = [Collection(event,x) for x in input]
        leptons = [(coll[j][i],j,i) for j in xrange(len(input)) for i in xrange(len(coll[j]))]
        if self.selector: leptons=filter(lambda (obj,j,i) : self.selector[j](obj), leptons)
        leptons.sort(key = self.sortkey, reverse = self.reverse)
        #electrons = Collection(event, "Electron")
        #muons = Collection(event, "Muon")
        jets = Collection(event, "Jet")
        taus = Collection(event, "Tau")

        if hasattr(event,'nGenPart'):
            genparts = Collection(event, "GenPart")

        if hasattr(event,'nLHEPart'):
            lheparts = Collection(event, "LHEPart")

        loose_leptons = []
        fakeable_leptons = []
        tight_leptons = []

        loose_jets = []
        fakeable_jets = []
        tight_jets = []

        n_loose_leptons = 0;
        veto_3l_loose = 0;
        veto_wz_loose = 0;
        n_fakeable_leptons = 0;
        veto_3l_fakeable = 0;
        veto_wz_fakeable = 0;
        n_tight_leptons = 0;
        veto_3l_tight = 0;
        veto_wz_tight = 0;

        if len(leptons) < 2:
            return False
        for i in range(0,len(leptons)):
            if abs(leptons[i][0].pdgId) == 13:
                if leptons[i][0].pt < 10:
                    continue
                if abs(leptons[i][0].eta) > 2.4:
                    continue

                # loose muon: nanoAOD after basic selection (pt > 3 && track.isNonnull && isLooseMuon)
                #if leptons[i][0].looseId:
                loose_leptons.append(i)
                n_loose_leptons+=1
                if n_loose_leptons==self.maxObjects and leptons[i][0].pt > 10:
                    veto_3l_loose==1
                if n_loose_leptons>self.maxObjects and leptons[i][0].pt > 10:
                    veto_wz_loose = 1

                if n_fakeable_leptons >= self.maxObjects and leptons[i][0].pt > 10:
                    veto_3l_fakeable = 1

                if n_tight_leptons >= self.maxObjects and leptons[i][0].pt > 10:
                    veto_3l_tight = 1
                # fakeable muon
                if leptons[i][0].tightId and leptons[i][0].pfRelIso04_all < 0.4:
                    fakeable_leptons.append(i)
                    n_fakeable_leptons+=1
                    if n_fakeable_leptons>self.maxObjects and leptons[i][0].pt > 10:
                        veto_wz_fakeable = 1
                        # tight muon
                        if leptons[i][0].tightId and leptons[i][0].pfRelIso04_all < 0.15:
                            tight_leptons.append(i)
                            n_tight_leptons+=1
                            if n_tight_leptons>self.maxObjects and leptons[i][0].pt > 10:
                                veto_wz_tight = 1
            elif abs(leptons[i][0].pdgId) == 11:
                if leptons[i][0].pt/leptons[i][0].eCorr < 10:
                    continue
                if abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) > 2.5:
                    continue

                if (abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) < 1.479 and abs(leptons[i][0].dz) < 0.1 and abs(leptons[i][0].dxy) < 0.05) or (abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) > 1.479 and abs(leptons[i][0].dz) < 0.2 and abs(leptons[i][0].dxy) < 0.1):
                    # loose electron
                    if leptons[i][0].cutBased >= 1:
                        loose_leptons.append(i)
                        n_loose_leptons+=1
                        if n_loose_leptons==self.maxObjects and leptons[i][0].pt > 10:
                            veto_3l_loose = 1
                        if n_loose_leptons>self.maxObjects and leptons[i][0].pt > 10:
                            veto_wz_loose = 1

                        if n_fakeable_leptons >= self.maxObjects and leptons[i][0].pt > 10:
                            veto_3l_fakeable = 1

                        if n_tight_leptons >= self.maxObjects and leptons[i][0].pt > 10:
                            veto_3l_tight = 1
                        # fakeable electron
                        if leptons[i][0].cutBased_HLTPreSel==1:
                            fakeable_leptons.append(i)
                            n_fakeable_leptons+=1
                            if n_fakeable_leptons>self.maxObjects and leptons[i][0].pt > 10:
                                veto_wz_fakeable = 1
                        # tight electron
                        if (leptons[i][0].cutBased > 3 and leptons[i][0].tightCharge == 2):
                            tight_leptons.append(i)
                            n_tight_leptons+=1
                            if n_tight_leptons>self.maxObjects and leptons[i][0].pt > 10:
                                veto_wz_tight = 1

        if n_loose_leptons < 2 or (veto_wz_tight == 1 and veto_wz_fakeable == 1 and veto_wz_loose == 1):
            return False

        # tau veto
        loose_tauVeto = 0
        fakeable_tauVeto = 0
        tight_tauVeto = 0
        if len(jets) < 2:
            return False
        for i in range(0,len(taus)):
            if (taus[i].pt > 18 and abs(taus[i].eta) < 2.3 and taus[i].idDecayMode and taus[i].idDecayModeNewDMs and taus[i].rawIso) < 5:
                tau_match_flag = False
                for j in range(0,len(loose_leptons)):
                    if deltaR(leptons[loose_leptons[j]][0].eta,leptons[loose_leptons[j]][0].phi,taus[i].eta,taus[i].phi) < 0.4:
                        tau_match_flag = True
                if tau_match_flag == False:
                    loose_tauVeto = 1

        for i in range(0,len(taus)):
            if (taus[i].pt > 18 and abs(taus[i].eta) < 2.3 and taus[i].idDecayMode and taus[i].idDecayModeNewDMs and taus[i].rawIso) < 5:
                tau_match_flag = False
                for j in range(0,len(fakeable_leptons)):
                    if deltaR(leptons[fakeable_leptons[j]][0].eta,leptons[fakeable_leptons[j]][0].phi,taus[i].eta,taus[i].phi) < 0.4:
                        tau_match_flag = True
                if tau_match_flag == False:
                    fakeable_tauVeto = 1

        for i in range(0,len(taus)):
            if (taus[i].pt > 18 and abs(taus[i].eta) < 2.3 and taus[i].idDecayMode and taus[i].idDecayModeNewDMs and taus[i].rawIso) < 5:
                tau_match_flag = False
                for j in range(0,len(tight_leptons)):
                    if deltaR(leptons[tight_leptons[j]][0].eta,leptons[tight_leptons[j]][0].phi,taus[i].eta,taus[i].phi) < 0.4:
                        tau_match_flag = True
                if tau_match_flag == False:
                    tight_tauVeto = 1


        # jets
        bveto = 0
        # jets correlated with loose leptons
        if len(jets) < 2:
            return False
        for i in range(0,len(jets)):
            if jets[i].pt > 20 and abs(jets[i].eta) < 2.4:
                if jets[i].btagCSVV2>0.9535:
                    bveto = 2 # bveto loose
                elif jets[i].btagCSVV2>0.8484:
                    bveto = 1 # bveto medium

            if jets[i].pt < 30:
                continue

            if abs(jets[i].eta) > 5.0:
                continue

            pass_lepton_dr_cut = True

            for j in range(0,len(loose_leptons)):

                if deltaR(leptons[loose_leptons[j]][0].eta,leptons[loose_leptons[j]][0].phi,jets[i].eta,jets[i].phi) < 0.5:

                    pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            loose_jets.append(i)

        # jets correlated with fakeable leptons
        for i in range(0,len(jets)):

            if jets[i].pt < 30:
                continue

            if abs(jets[i].eta) > 5.0:
                continue

            pass_lepton_dr_cut = True

            for j in range(0,len(fakeable_leptons)):

                if deltaR(leptons[fakeable_leptons[j]][0].eta,leptons[fakeable_leptons[j]][0].phi,jets[i].eta,jets[i].phi) < 0.5:

                    pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            fakeable_jets.append(i)

        # jets correlated with tight leptons
        for i in range(0,len(jets)):

            if jets[i].pt < 30:
                continue

            if abs(jets[i].eta) > 5.0:
                continue

            pass_lepton_dr_cut = True

            for j in range(0,len(tight_leptons)):

                if deltaR(leptons[tight_leptons[j]][0].eta,leptons[tight_leptons[j]][0].phi,jets[i].eta,jets[i].phi) < 0.5:

                    pass_lepton_dr_cut = False

            if not pass_lepton_dr_cut:
                continue

            tight_jets.append(i)

        n_loose_jets = 0
        n_fakeable_jets = 0
        n_tight_jets = 0

        if len(loose_jets) < 2 and len(fakeable_jets) < 2 and len(tight_jets) < 2:
            return False
        else:
            n_loose_jets = len(loose_jets)
            n_fakeable_jets = len(fakeable_jets)
            n_tight_jets = len(tight_jets)

        # decide whether lepton real
        isprompt_mask = (1 << 0) #isPrompt
        isdirectprompttaudecayproduct_mask = (1 << 5) #isDirectPromptTauDecayProduct

        lepton_idx=[-99,-99,-99,-99,-99,-99,-99,-99,-99]
        lepton_pdg_id=[-99,-99,-99,-99,-99,-99,-99,-99,-99]
        lepton_pt=[-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.]
        lepton_phi=[-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.]
        lepton_eta=[-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.]
        lepton_mass=[-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.]
        lepton_real=[0,0,0,0,0,0,0,0,0]
        lepton_mishits=[0,0,0,0,0,0,0,0,0]
        lepton_tkIsoId=[0,0,0,0,0,0,0,0,0]

        # store leptons information: 0 1 2 tight leptons, 3 4 5 fakeable leptons, 6 7 8 loose leptons
        # loose leptons
        for i in range(0,len(loose_leptons)):
            if i >= self.maxObjects:
                break
            lepton_idx[i+6] = loose_leptons[i]
            if abs(leptons[loose_leptons[i]][0].pdgId) == 13:
                PID = 13
                lepton_tkIsoId[i+6] = leptons[loose_leptons[i]][0].tkIsoId
            elif abs(leptons[loose_leptons[i]][0].pdgId) == 11:
                PID = 11
                lepton_mishits[i+6] = leptons[loose_leptons[i]][0].lostHits

            lepton_pdg_id[i+6] = leptons[loose_leptons[i]][0].pdgId
            lepton_pt[i+6] = leptons[loose_leptons[i]][0].pt
            lepton_phi[i+6] = leptons[loose_leptons[i]][0].phi
            lepton_eta[i+6] = leptons[loose_leptons[i]][0].eta
            lepton_mass[i+6] = leptons[loose_leptons[i]][0].mass

            try:
                for j in range(0,len(genparts)):
                    if genparts[j].pt > 5 and abs(genparts[j].pdgId) == PID and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(leptons[loose_leptons[i]][0].eta,leptons[loose_leptons[i]][0].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                        lepton_real[i+6] = 1
            except:
                pass
        # fakeable leptons
        for i in range(0,len(fakeable_leptons)):
            if i >= self.maxObjects:
                break
            lepton_idx[i+3] = fakeable_leptons[i]
            if abs(leptons[fakeable_leptons[i]][0].pdgId) == 13:
                PID = 13
                lepton_tkIsoId[i+3] = leptons[fakeable_leptons[i]][0].tkIsoId
            elif abs(leptons[fakeable_leptons[i]][0].pdgId) == 11:
                PID = 11
                lepton_mishits[i+3] = leptons[fakeable_leptons[i]][0].lostHits

            lepton_pdg_id[i+3] = leptons[fakeable_leptons[i]][0].pdgId
            lepton_pt[i+3] = leptons[fakeable_leptons[i]][0].pt
            lepton_phi[i+3] = leptons[fakeable_leptons[i]][0].phi
            lepton_eta[i+3] = leptons[fakeable_leptons[i]][0].eta
            lepton_mass[i+6] = leptons[fakeable_leptons[i]][0].mass
            try:
                for j in range(0,len(genparts)):
                    if genparts[j].pt > 5 and abs(genparts[j].pdgId) == PID and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(leptons[fakeable_leptons[i]][0].eta,leptons[fakeable_leptons[i]][0].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                        lepton_real[i+3] = 1
            except:
                pass
        # tight lepton
        for i in range(0,len(tight_leptons)):
            if i >= self.maxObjects:
                break
            lepton_idx[i] = tight_leptons[i]
            if abs(leptons[tight_leptons[i]][0].pdgId) == 13:
                PID = 13
                lepton_tkIsoId[i] = leptons[tight_leptons[i]][0].tkIsoId
            elif abs(leptons[tight_leptons[i]][0].pdgId) == 11:
                PID = 11
                lepton_mishits[i] = leptons[tight_leptons[i]][0].lostHits

            lepton_pdg_id[i] = leptons[tight_leptons[i]][0].pdgId
            lepton_pt[i] = leptons[tight_leptons[i]][0].pt
            lepton_phi[i] = leptons[tight_leptons[i]][0].phi
            lepton_eta[i] = leptons[tight_leptons[i]][0].eta
            lepton_mass[i+6] = leptons[tight_leptons[i]][0].mass

            try:
                for j in range(0,len(genparts)):
                    if genparts[j].pt > 5 and abs(genparts[j].pdgId) == PID and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(leptons[tight_leptons[i]][0].eta,leptons[tight_leptons[i]][0].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                        lepton_real[i] = 1
            except:
                pass

        # store jets information: 0 1 2 jets correlated with tight leptons; 3 4 5 jets correlated with fakeable leptons; 6 7 8 jets correlated with loose lepton
        jet_idx=[-99,-99,-99,-99,-99,-99,-99,-99,-99]
        jet_id=[-99,-99,-99,-99,-99,-99,-99,-99,-99]
        jet_pt=[-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.]
        jet_eta=[-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.]
        jet_phi=[-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.]
        jet_mass=[-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.]
        jet_btagCSVV2=[-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.]

        for i in range(0,len(tight_jets)):
            if i < self.maxObjects:
                jet_idx[i]=tight_jets[i]
                jet_id[i]=jets[tight_jets[i]].jetId
                jet_pt[i]=jets[tight_jets[i]].pt
                jet_eta[i]=jets[tight_jets[i]].eta
                jet_phi[i]=jets[tight_jets[i]].phi
                jet_mass[i]=jets[tight_jets[i]].mass
                jet_btagCSVV2[i]=jets[tight_jets[i]].btagCSVV2
            else:
                break

        for i in range(0,len(fakeable_jets)):
            if i < self.maxObjects:
                jet_idx[i+3]=fakeable_jets[i]
                jet_id[i+3]=jets[fakeable_jets[i]].jetId
                jet_pt[i+3]=jets[fakeable_jets[i]].pt
                jet_eta[i+3]=jets[fakeable_jets[i]].eta
                jet_phi[i+3]=jets[fakeable_jets[i]].phi
                jet_mass[i+3]=jets[fakeable_jets[i]].mass
                jet_btagCSVV2[i+3]=jets[fakeable_jets[i]].btagCSVV2
            else:
                break

        for i in range(0,len(loose_jets)):
            if i < self.maxObjects:
                jet_idx[i+6]=loose_jets[i]
                jet_id[i+6]=jets[loose_jets[i]].jetId
                jet_pt[i+6]=jets[loose_jets[i]].pt
                jet_eta[i+6]=jets[loose_jets[i]].eta
                jet_phi[i+6]=jets[loose_jets[i]].phi
                jet_mass[i+6]=jets[loose_jets[i]].mass
                jet_btagCSVV2[i+6]=jets[loose_jets[i]].btagCSVV2
            else:
                break
        self.out.fillBranch("run",event.run)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("event",event.event)

        if hasattr(event,'Pileup_nPU'):
            self.out.fillBranch("npu",event.Pileup_nPU)
        else:
            self.out.fillBranch("npu",0)

        if hasattr(event,'Pileup_nTrueInt'):
            self.out.fillBranch("ntruepu",event.Pileup_nTrueInt)
        else:
            self.out.fillBranch("ntruepu",0)

        self.out.fillBranch("npvs",event.PV_npvs)

        if hasattr(event,'Generator_weight'):
            self.out.fillBranch("gen_weight",event.Generator_weight)
        else:
            self.out.fillBranch("gen_weight",0)

        self.out.fillBranch("tight_tauVeto",tight_tauVeto)
        self.out.fillBranch("fakeable_tauVeto",fakeable_tauVeto)
        self.out.fillBranch("loose_tauVeto",loose_tauVeto)
        self.out.fillBranch("n_tight_leptons",n_tight_leptons)
        self.out.fillBranch("n_fakeable_leptons",n_fakeable_leptons)
        self.out.fillBranch("n_loose_leptons",n_loose_leptons)
        self.out.fillBranch("veto_3l_tight",veto_3l_tight)
        self.out.fillBranch("veto_3l_fakeable",veto_3l_fakeable)
        self.out.fillBranch("veto_3l_loose",veto_3l_loose)
        self.out.fillBranch("veto_wz_tight",veto_wz_tight)
        self.out.fillBranch("veto_wz_fakeable",veto_wz_fakeable)
        self.out.fillBranch("veto_wz_loose",veto_wz_loose)
        self.out.fillBranch("lepton_pdg_id",lepton_pdg_id)
        self.out.fillBranch("lepton_pt",lepton_pt)
        self.out.fillBranch("lepton_eta",lepton_eta)
        self.out.fillBranch("lepton_phi",lepton_phi)
        self.out.fillBranch("lepton_mass",lepton_mass)
        self.out.fillBranch("lepton_real",lepton_real)
        self.out.fillBranch("lepton_idx",lepton_idx)
        self.out.fillBranch("lepton_mishits",lepton_mishits)
        self.out.fillBranch("lepton_tkIsoId",lepton_tkIsoId)
        print lepton_pt
        mll=[-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.]
        # tight leptons - mll : 0 1 2 : mll mll02 mll12
        if lepton_pt[0] > -99. and lepton_pt[1] > -99.:
            mll[0]=(leptons[tight_leptons[0]][0].p4() + leptons[tight_leptons[1]][0].p4()).M()
        if lepton_pt[0] > -99. and lepton_pt[2] > -99.:
            mll[1]=(leptons[tight_leptons[0]][0].p4() + leptons[tight_leptons[2]][0].p4()).M()
        if lepton_pt[1] > -99. and lepton_pt[2] > -99.:
            mll[2]=(leptons[tight_leptons[1]][0].p4() + leptons[tight_leptons[2]][0].p4()).M()
        # fakeable leptons - mll : 3 4 5 : mll mll02 mll12
        if lepton_pt[0+3] > -99. and lepton_pt[1+3] > -99.:
            mll[3]=(leptons[fakeable_leptons[0]][0].p4() + leptons[fakeable_leptons[1]][0].p4()).M()
        if lepton_pt[0+3] > -99. and lepton_pt[2+3] > -99.:
            mll[4]=(leptons[fakeable_leptons[0]][0].p4() + leptons[fakeable_leptons[2]][0].p4()).M()
        if lepton_pt[1+3] > -99. and lepton_pt[2+3] > -99.:
            mll[5]=(leptons[fakeable_leptons[1]][0].p4() + leptons[fakeable_leptons[2]][0].p4()).M()
        # loose leptons - mll : 6 7 8 : mll mll02 mll12
        if lepton_pt[0+6] > -99. and lepton_pt[1+6] > -99.:
            mll[6]=(leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[1]][0].p4()).M()
        if lepton_pt[0+6] > -99. and lepton_pt[2+6] > -99.:
            mll[7]=(leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[2]][0].p4()).M()
        if lepton_pt[1+6] > -99. and lepton_pt[2+6] > -99.:
            mll[8]=(leptons[loose_leptons[1]][0].p4() + leptons[loose_leptons[2]][0].p4()).M()
        self.out.fillBranch("mll",mll)

        self.out.fillBranch("bveto",bveto)
        self.out.fillBranch("n_tight_jets",n_tight_jets)
        self.out.fillBranch("n_fakeable_jets",n_fakeable_jets)
        self.out.fillBranch("n_loose_jets",n_loose_jets)
        self.out.fillBranch("jet_id",jet_id)
        self.out.fillBranch("jet_pt",jet_pt)
        self.out.fillBranch("jet_phi",jet_phi)
        self.out.fillBranch("jet_mass",jet_mass)
        self.out.fillBranch("jet_eta",jet_eta)
        self.out.fillBranch("jet_idx",jet_idx)
        self.out.fillBranch("jet_btagCSVV2",jet_btagCSVV2)

        mjj=[-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.,-99.]
        # tight jets - mjj : 0 1 2 : mjj mjj02 mjj12
        if jet_pt[0] > -99. and jet_pt[1] > -99.:
            mjj[0]=(jets[tight_jets[0]].p4() + jets[tight_jets[1]].p4()).M()
        if jet_pt[0] > -99. and jet_pt[2] > -99.:
            mjj[1]=(jets[tight_jets[0]].p4() + jets[tight_jets[2]].p4()).M()
        if jet_pt[1] > -99. and jet_pt[2] > -99.:
            mjj[2]=(jets[tight_jets[1]].p4() + jets[tight_jets[2]].p4()).M()
        # fakeable jets - mjj : 3 4 5 : mjj mjj02 mjj12
        if jet_pt[0+3] > -99. and jet_pt[1+3] > -99.:
            mjj[3]=(jets[fakeable_jets[0]].p4() + jets[fakeable_jets[1]].p4()).M()
        if jet_pt[0+3] > -99. and jet_pt[2+3] > -99.:
            mjj[4]=(jets[fakeable_jets[0]].p4() + jets[fakeable_jets[2]].p4()).M()
        if jet_pt[1+3] > -99. and jet_pt[2+3] > -99.:
            mjj[5]=(jets[fakeable_jets[1]].p4() + jets[fakeable_jets[2]].p4()).M()
        # loose jets - mjj : 6 7 8 : mjj mjj02 mjj12
        if jet_pt[0+6] > -99. and jet_pt[1+6] > -99.:
            mjj[6]=(jets[loose_jets[0]].p4() + jets[loose_jets[1]].p4()).M()
        if jet_pt[0+6] > -99. and jet_pt[2+6] > -99.:
            mjj[7]=(jets[loose_jets[0]].p4() + jets[loose_jets[2]].p4()).M()
        if jet_pt[1+6] > -99. and jet_pt[2+6] > -99.:
            mjj[8]=(jets[loose_jets[1]].p4() + jets[loose_jets[2]].p4()).M()
        self.out.fillBranch("mjj",mjj)

        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("met_phi",event.MET_phi)
        # tight mt
        if lepton_pt[0] > -99. and  lepton_pt[1] > -99.:
            self.out.fillBranch("mt0",sqrt(2*(leptons[tight_leptons[0]][0].p4()+leptons[tight_leptons[1]][0].p4()).Pt()*event.MET_pt*(1 - cos(event.MET_phi - (leptons[tight_leptons[0]][0].p4()+leptons[tight_leptons[1]][0].p4()).Phi()))))
        else:
            self.out.fillBranch("mt0",-99.)
        # fakeable mt
        if lepton_pt[0+3] > -99. and  lepton_pt[1+3] > -99.:
            self.out.fillBranch("mt1",sqrt(2*(leptons[fakeable_leptons[0]][0].p4()+leptons[fakeable_leptons[1]][0].p4()).Pt()*event.MET_pt*(1 - cos(event.MET_phi - (leptons[fakeable_leptons[0]][0].p4()+leptons[fakeable_leptons[1]][0].p4()).Phi()))))
        else:
            self.out.fillBranch("mt1",-99.)
        # loose mt
        if lepton_pt[0+6] > -99. and  lepton_pt[1+6] > -99.:
            self.out.fillBranch("mt2",sqrt(2*(leptons[loose_leptons[0]][0].p4()+leptons[loose_leptons[1]][0].p4()).Pt()*event.MET_pt*(1 - cos(event.MET_phi - (leptons[loose_leptons[0]][0].p4()+leptons[loose_leptons[1]][0].p4()).Phi()))))
        else:
            self.out.fillBranch("mt2",-99.)

        self.out.fillBranch("puppimet",event.PuppiMET_pt)
        self.out.fillBranch("puppimet_phi",event.PuppiMET_phi)

        return True

sswwModule = lambda : sswwProducer(maxObjects=3)
sswwModuleData = lambda : sswwProducer(maxObjects=3,isData = True)
