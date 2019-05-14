import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

leptonsize=3
jetsize=3
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
        self.out.branch("lepton_wp",  "I"); # 0 means tight, 1 means fakeable, 2 means loose
        self.out.branch("gen_weight",  "F");
        #self.out.branch("trigger", "B", lenVar="triggersize");

        self.out.branch("tauVeto","B");
        self.out.branch("nleptons","I");
        self.out.branch("lepton_pdg_id",  "I", lenVar="leptonsize");
        self.out.branch("lepton_pt",  "F", lenVar="leptonsize");
        self.out.branch("lepton_phi",  "F", lenVar="leptonsize");
        self.out.branch("lepton_eta",  "F", lenVar="leptonsize");
        self.out.branch("lepton_real",  "B", lenVar="leptonsize");
        self.out.branch("lepton_mishits",  "I", lenVar="leptonsize");

        self.out.branch("mll",  "F");
        self.out.branch("mll02",  "F");
        self.out.branch("mll12",  "F");

        '''
        self.out.branch("lep1_pdg_id",  "I");
        self.out.branch("lep1_pt",  "F");
        self.out.branch("lep1_phi",  "F");
        self.out.branch("lep1_eta",  "F");
        self.out.branch("lep2_pdg_id",  "I");
        self.out.branch("lep2_pt",  "F");
        self.out.branch("lep2_phi",  "F");
        self.out.branch("lep2_eta",  "F");
        self.out.branch("is_lep0_real",  "B");
        self.out.branch("is_lep1_real",  "B");
        self.out.branch("is_lep2_real",  "B");
        self.out.branch("lep0_mishits",  "B");
        self.out.branch("lep1_mishits",  "B");
        self.out.branch("lep2_mishits",  "B");
        '''
        self.out.branch("bveto_tight","B");
        self.out.branch("bveto_medium","B");
        self.out.branch("njets","I");
        self.out.branch("jet_pt",  "F", lenVar="jetsize");
        self.out.branch("jet_phi",  "F", lenVar="jetsize");
        self.out.branch("jet_eta",  "F", lenVar="jetsize");
        self.out.branch("jet_btagCSVV2",  "F", lenVar="jetsize");

        self.out.branch("detajj","F");
        self.out.branch("mjj","F");
        self.out.branch("met",  "F");
        self.out.branch("mt",  "F");
        self.out.branch("mt1",  "F");
        self.out.branch("puppimet",  "F");

        self.out.branch("zepp0","F");
        self.out.branch("zepp1","F");

        '''
        self.out.branch("jet1_pt",  "F");
        self.out.branch("jet1_phi",  "F");
        self.out.branch("jet1_eta",  "F");
        self.out.branch("jet2_pt",  "F");
        self.out.branch("jet2_phi",  "F");
        self.out.branch("jet2_eta",  "F");
        '''
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
            if not (event.HLT_Mu17_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL or event.HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL or  event.HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL or
            event.HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL or event.HLT_Mu8_TrkIsoVVL_Ele17_CaloIdL_TrackIdL_IsoVL or event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL or event.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL or event.HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ or event.HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ or event.HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ or event.HLT_DoubleEle24_22_eta2p1_WPLoose_Gsf or event.HLT_IsoMu20 or event.HLT_IsoMu22 or event.HLT_IsoMu24 or event.HLT_IsoMu27 or event.HLT_IsoTkMu20 or event.HLT_IsoTkMu22 or event.HLT_IsoTkMu24 or event.HLT_IsoTkMu27 or event.HLT_Mu45_eta2p1 or event.HLT_Mu50 or event.HLT_Ele25_eta2p1_WPTight_Gsf or event.HLT_Ele27_eta2p1_WPLoose_Gsf or event.HLT_Ele27_WPTight_Gsf or event.HLT_Ele27_WPTight_Gsf or event.HLT_Ele35_WPLoose_Gsf):
                return False
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

        tight_leptons = []

        #fakeable_leptons = []

        #loose_leptons = []
        tight_jets = []

        nleptons = 0;
        if len(leptons) < 2:
            return False
        for i in range(0,len(leptons)):
            if abs(leptons[i][0].pdgId) == 13:
                if leptons[i][0].pt < 10:
                    continue
                if abs(leptons[i][0].eta) > 2.4:
                    continue
                #if leptons[i][0].looseId:
                #    loose_leptons.append(i)
                #if leptons[i][0].tightId and leptons[i][0].pfRelIso04_all < 0.4 and :
                #    fakeable_leptons.append(i)
                if leptons[i][0].tightId and leptons[i][0].pfRelIso04_all < 0.15:
                    tight_leptons.append(i)
                    nleptons+=1
            elif abs(leptons[i][0].pdgId) == 11:
                if leptons[i][0].pt/leptons[i][0].eCorr < 10:
                    continue
                if abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) > 2.5:
                    continue
                if (abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) < 1.479 and abs(leptons[i][0].dz) < 0.1 and abs(leptons[i][0].dxy) < 0.05) or (abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) > 1.479 and abs(leptons[i][0].dz) < 0.2 and abs(leptons[i][0].dxy) < 0.1):
                    #if leptons[i][0].cutBased >= 1:
                    #    loose_leptons.append(i)
                    #if leptons[i][0].cutBased_HLTPreSel==1:
                    #    fakeable_leptons.append(i)
                    if (leptons[i][0].cutBased > 3 and leptons[i][0].tightCharge == 2):
                        tight_leptons.append(i)
                        nleptons+=1
            if nleptons > self.maxObjects:
                if leptons[i][0].pt >= 10:
                    return False
                elif leptons[i][0].pt < 10:
                    break

        if (len(tight_leptons) > self.maxObjects or len(tight_leptons) < 2):
            return False

        tauVeto = 0
        for i in range(0,len(taus)):
            if (taus[i].pt > 18 and abs(taus[i].eta) < 2.3 and taus[i].idDecayMode and taus[i].idDecayModeNewDMs and taus[i].rawIso < 5 and deltaR(leptons[tight_leptons[0]][0].eta,leptons[tight_leptons[0]][0].phi,taus[i].eta,taus[i].phi) > 0.4 and deltaR(leptons[tight_leptons[1]][0].eta,leptons[tight_leptons[1]][0].phi,taus[i].eta,taus[i].phi) > 0.4):
                tauVeto = 1

        njets = 0

        bveto_medium = 0
        bveto_tight = 0
        if len(jets) < 2:
            return False
        for i in range(0,len(jets)):
            if jets[i].pt > 20 and abs(jets[i].eta) < 2.4:
                if jets[i].btagCSVV2>0.9535:
                    bveto_tight = 1
                    bveto_medium = 1
                elif jets[i].btagCSVV2>0.8484:
                    bveto_medium = 1

            if jets[i].pt < 30:
                continue

            if abs(jets[i].eta) > 5.0:
                continue

            pass_lepton_dr_cut = True

            for j in range(0,len(tight_leptons)):

                if deltaR(leptons[tight_leptons[j]][0].eta,leptons[tight_leptons[j]][0].phi,jets[i].eta,jets[i].phi) < 0.5:
                    pass_lepton_dr_cut = False
            '''
            for j in range(0,len(fakeable_leptons)):

                if deltaR(leptons[fakeable_leptons[j]][0].eta,leptons[fakeable_leptons[j]][0].phi,jets[i].eta,jets[i].phi) < 0.5:

                    pass_lepton_dr_cut = False

            for j in range(0,len(loose_leptons)):

                if deltaR(leptons[loose_leptons[j]][0].eta,leptons[loose_leptons[j]][0].phi,jets[i].eta,jets[i].phi) < 0.5:

                     pass_lepton_dr_cut = False
            '''
            if not pass_lepton_dr_cut:
                continue

            tight_jets.append(i)

        if len(tight_jets) < 2:
            return False

        isprompt_mask = (1 << 0) #isPrompt
        isdirectprompttaudecayproduct_mask = (1 << 5) #isDirectPromptTauDecayProduct

        lepton_pdg_id=[-99,-99,-99]
        lepton_pt=[-99.,-99.,-99.]
        lepton_phi=[-99.,-99.,-99.]
        lepton_eta=[-99.,-99.,-99.]
        lepton_real=[0,0,0]
        lepton_mishits=[0,0,0]

        for i in range(0,len(tight_leptons)):
            if abs(leptons[tight_leptons[i]][0].pdgId) == 13:
                PID = 13
            elif abs(leptons[tight_leptons[i]][0].pdgId) == 11:
                PID = 11
                lepton_mishits[i] = leptons[tight_leptons[i]][0].lostHits

            lepton_pdg_id[i] = leptons[tight_leptons[i]][0].pdgId
            lepton_pt[i] = leptons[tight_leptons[i]][0].pt
            lepton_phi[i] = leptons[tight_leptons[i]][0].phi
            lepton_eta[i] = leptons[tight_leptons[i]][0].eta

            try:
                for j in range(0,len(genparts)):
                    if genparts[j].pt > 5 and abs(genparts[j].pdgId) == PID and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(leptons[tight_leptons[i]][0].eta,leptons[tight_leptons[i]][0].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                        lepton_real[i] = 1
            except:
                pass

        jet_pt=[-99.,-99.,-99.]
        jet_eta=[-99.,-99.,-99.]
        jet_phi=[-99.,-99.,-99.]
        jet_btagCSVV2=[-99.,-99.,-99.]

        for i in range(0,len(jets)):
            if i < 3:
                jet_pt[i]=jets[i].pt
                jet_eta[i]=jets[i].eta
                jet_phi[i]=jets[i].phi
                jet_btagCSVV2[i]=jets[i].btagCSVV2
            else:
                break

        self.out.fillBranch("event",event.event)
        self.out.fillBranch("lumi",event.luminosityBlock)
        self.out.fillBranch("run",event.run)
        self.out.fillBranch("npvs",event.PV_npvs)
        self.out.fillBranch("lepton_wp",0) # 0 means tight, 1 means fakeable, 2 means loose
        #self.out.fillBranch("trigger",trigger)

        if hasattr(event,'Generator_weight'):
            self.out.fillBranch("gen_weight",event.Generator_weight)
        else:
            self.out.fillBranch("gen_weight",0)

        if hasattr(event,'Pileup_nPU'):
            self.out.fillBranch("npu",event.Pileup_nPU)
        else:
            self.out.fillBranch("npu",0)

        if hasattr(event,'Pileup_nTrueInt'):
            self.out.fillBranch("ntruepu",event.Pileup_nTrueInt)
        else:
            self.out.fillBranch("ntruepu",0)

        self.out.fillBranch("tauVeto",tauVeto)
        self.out.fillBranch("nleptons",nleptons)
        self.out.fillBranch("lepton_pdg_id",lepton_pdg_id)
        self.out.fillBranch("lepton_pt",lepton_pt)
        self.out.fillBranch("lepton_eta",lepton_eta)
        self.out.fillBranch("lepton_phi",lepton_phi)
        self.out.fillBranch("lepton_real",lepton_real)
        self.out.fillBranch("lepton_mishits",lepton_mishits)

        if lepton_pt[0] > -99. and lepton_pt[1] > -99.:
            self.out.fillBranch("mll",(leptons[tight_leptons[0]][0].p4() + leptons[tight_leptons[1]][0].p4()).M())
        else:
            self.out.fillBranch("mll",-99.)

        if lepton_pt[0] > -99. and lepton_pt[2] > -99.:
            self.out.fillBranch("mll02",(leptons[tight_leptons[0]][0].p4() + leptons[tight_leptons[2]][0].p4()).M())
        else:
            self.out.fillBranch("mll02",-99.)

        if lepton_pt[1] > -99. and lepton_pt[2] > -99.:
            self.out.fillBranch("mll12",(leptons[tight_leptons[1]][0].p4() + leptons[tight_leptons[2]][0].p4()).M())
        else:
            self.out.fillBranch("mll12",-99.)

        self.out.fillBranch("bveto_tight",bveto_tight)
        self.out.fillBranch("bveto_medium",bveto_medium)
        self.out.fillBranch("njets",njets)
        self.out.fillBranch("jet_pt",jet_pt)
        self.out.fillBranch("jet_phi",jet_phi)
        self.out.fillBranch("jet_eta",jet_eta)
        self.out.fillBranch("jet_btagCSVV2",jet_btagCSVV2)

        self.out.fillBranch("detajj",(jets[tight_jets[0]].eta - jets[tight_jets[1]].eta))
        self.out.fillBranch("mjj",(jets[tight_jets[0]].p4() + jets[tight_jets[1]].p4()).M())
        self.out.fillBranch("met",event.MET_pt)
        if leptons[tight_leptons[0]][0].pdgId == 11:
            self.out.fillBranch("mt",sqrt(2*leptons[tight_leptons[0]][0].pt/leptons[tight_leptons[0]][0].eCorr*event.MET_pt*(1 - cos(event.MET_phi - leptons[tight_leptons[0]][0].phi))))
        else:
            self.out.fillBranch("mt",sqrt(2*leptons[tight_leptons[0]][0].pt*event.MET_pt*(1 - cos(event.MET_phi - leptons[tight_leptons[0]][0].phi))))

        if leptons[tight_leptons[1]][0].pdgId == 11:
            self.out.fillBranch("mt1",sqrt(2*leptons[tight_leptons[1]][0].pt/leptons[tight_leptons[1]][0].eCorr*event.MET_pt*(1 - cos(event.MET_phi - leptons[tight_leptons[1]][0].phi))))
        else:
            self.out.fillBranch("mt1",sqrt(2*leptons[tight_leptons[1]][0].pt*event.MET_pt*(1 - cos(event.MET_phi - leptons[tight_leptons[1]][0].phi))))

        self.out.fillBranch("puppimet",event.PuppiMET_pt)

        if abs(jets[tight_jets[0]].eta - jets[tight_jets[1]].eta) > 0.:
            self.out.fillBranch("zepp0",abs((leptons[tight_leptons[0]][0].eta-(jets[tight_jets[0]].eta+jets[tight_jets[1]].eta)/2.)/(jets[tight_jets[0]].eta - jets[tight_jets[1]].eta)))
        else:
            self.out.fillBranch("zepp0",-99.)

        if abs(jets[tight_jets[0]].eta - jets[tight_jets[1]].eta) > 0.:
            self.out.fillBranch("zepp1",abs((leptons[tight_leptons[1]][0].eta-(jets[tight_jets[0]].eta+jets[tight_jets[1]].eta)/2.)/(jets[tight_jets[0]].eta - jets[tight_jets[1]].eta)))
        else:
            self.out.fillBranch("zepp1",-99.)

        return True

sswwModule = lambda : sswwProducer(maxObjects=3)
sswwModuleData = lambda : sswwProducer(maxObjects=3,isData = True)
