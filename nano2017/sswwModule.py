import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

nLepton=2
nJet=3
#triggersize=32

class sswwProducer(Module):
    def __init__(self,sortkey = lambda x : x.pt,reverse=True,selector=None,minObjects=None,maxObjects=None, isData = False,isWZ = False):
        self.sortkey = lambda (obj,j,i) : sortkey(obj)
        self.reverse = reverse
        self.selector = [(selector[coll] if coll in selector else (lambda x: True)) for coll in self.input] if selector else None # pass dict([(collection_name,lambda obj : selection(obj)])
        self.minObjects = minObjects # save only the first maxObjects objects passing the selection in the merged collection
        self.maxObjects = maxObjects # save only the first maxObjects objects passing the selection in the merged collection
        self.isData = isData
        self.isWZ = isWZ
        pass
    def beginJob(self):
        nLepton=self.maxObjects
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

        self.out.branch("tauVeto","B");
        self.out.branch("n_tight_leptons","I");
        self.out.branch("n_fakeable_leptons","I");
        self.out.branch("n_loose_leptons","I");
        self.out.branch("lepton_idx",  "I", lenVar="nLepton");
        self.out.branch("lepton_pdg_id",  "I", lenVar="nLepton");
        self.out.branch("lepton_tight",  "B", lenVar="nLepton");
        self.out.branch("lepton_fakeable",  "B", lenVar="nLepton");
        self.out.branch("lepton_pt",  "F", lenVar="nLepton");
        self.out.branch("lepton_eta",  "F", lenVar="nLepton");
        self.out.branch("lepton_phi",  "F", lenVar="nLepton");
        self.out.branch("lepton_mass",  "F", lenVar="nLepton");
        self.out.branch("lepton_real",  "B", lenVar="nLepton");
        self.out.branch("lepton_mishits",  "I", lenVar="nLepton");
        self.out.branch("lepton_tkIsoId",  "I", lenVar="nLepton");
        self.out.branch("lepton_softmu",  "B", lenVar="nLepton");
        self.out.branch("mll",  "F");

        self.out.branch("bveto","I");
        self.out.branch("n_loose_jets","I");
        self.out.branch("jet_idx",  "I", lenVar="nJet");
        self.out.branch("jet_id",  "I", lenVar="nJet");
        self.out.branch("jet_pt",  "F", lenVar="nJet");
        self.out.branch("jet_eta",  "F", lenVar="nJet");
        self.out.branch("jet_phi",  "F", lenVar="nJet");
        self.out.branch("jet_mass",  "F", lenVar="nJet");
        self.out.branch("jet_btagCSVV2",  "F", lenVar="nJet");
        self.out.branch("mjj","F", lenVar="nJet");
        self.out.branch("detajj","F", lenVar="nJet");

        self.out.branch("met",  "F");
        self.out.branch("met_phi",  "F");
        self.out.branch("mt",  "F");
        self.out.branch("mt2",  "F");
        self.out.branch("puppimet",  "F");
        self.out.branch("puppimet_phi",  "F");

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
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

        is_fakeable = []
        is_tight = []

        loose_jets = []

        n_loose_leptons = 0;
        n_fakeable_leptons = 0;
        n_tight_leptons = 0;

        if len(leptons) < 1:
            return False
        for i in range(0,len(leptons)):
            is_fakeable_id=False
            is_tight_id=False

            if abs(leptons[i][0].pdgId) == 13:
                if leptons[i][0].pt < 10:
                    continue
                if abs(leptons[i][0].eta) > 2.4:
                    continue
                # loose muon: nanoAOD after basic selection (pt > 3 && track.isNonnull && isLooseMuon)
                #if leptons[i][0].looseId:
                loose_leptons.append(i)
                n_loose_leptons+=1
                if len(loose_leptons) > self.maxObjects:
                    return False
                # fakeable muon
                if leptons[i][0].tightId and leptons[i][0].pfRelIso04_all < 0.4:
                    is_fakeable_id=True
                    n_fakeable_leptons+=1

                    # tight muon
                    if leptons[i][0].tightId and leptons[i][0].pfRelIso04_all < 0.15:
                        is_tight_id=True
                        n_tight_leptons+=1

                is_fakeable.append(is_fakeable_id)
                is_tight.append(is_tight_id)

            elif abs(leptons[i][0].pdgId) == 11:
                if leptons[i][0].pt/leptons[i][0].eCorr < 10:
                    continue
                if abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) > 2.5:
                    continue
                if (abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) < 1.479 and abs(leptons[i][0].dz) < 0.1 and abs(leptons[i][0].dxy) < 0.05) or (abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) > 1.479 and abs(leptons[i][0].dz) < 0.2 and abs(leptons[i][0].dxy) < 0.1):
                    # loose electron
                    if leptons[i][0].cutBased >= 1:
                        n_loose_leptons+=1
                        loose_leptons.append(i)

                        # fakeable electron
                        if leptons[i][0].cutBased_HLTPreSel==1:
                            is_fakeable_id=True
                            n_fakeable_leptons+=1

                        # tight electron
                        if (leptons[i][0].cutBased > 3 and leptons[i][0].tightCharge == 2):
                            is_tight_id=True
                            n_tight_leptons+=1

                        is_fakeable.append(is_fakeable_id)
                        is_tight.append(is_tight_id)

        if len(loose_leptons) > self.maxObjects or len(loose_leptons) < self.minObjects:
            return False
        if n_loose_leptons+n_tight_leptons+n_fakeable_leptons <= self.minObjects:
            return False
        if self.isWZ:
            if not(n_fakeable_leptons == 3) and not(n_tight_leptons == 3):
                return False
        # tau veto
        tauVeto = False
        for i in range(0,len(taus)):
            if (taus[i].pt > 18 and abs(taus[i].eta) < 2.3 and taus[i].idDecayMode and taus[i].idDecayModeNewDMs and taus[i].rawIso) < 5:
                tau_match_flag = False
                for j in range(0,len(loose_leptons)):
                    if deltaR(leptons[loose_leptons[j]][0].eta,leptons[loose_leptons[j]][0].phi,taus[i].eta,taus[i].phi) < 0.4:
                        tau_match_flag = True
                if tau_match_flag == False:
                    tauVeto = True


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

            # actually jet related lepton maybe not loose
            loose_jets.append(i)

        n_loose_jets = 0

        if len(loose_jets) < 2:
            return False
        else:
            n_loose_jets = len(loose_jets)

        # decide whether lepton real
        isprompt_mask = (1 << 0) #isPrompt
        isdirectprompttaudecayproduct_mask = (1 << 5) #isDirectPromptTauDecayProduct

        if self.isWZ:
            lepton_idx=[-99,-99,-99]
            lepton_pdg_id=[-99,-99,-99]
            lepton_tight=[False,False,False]
            lepton_fakeable=[False,False,False]
            lepton_pt=[-99.,-99.,-99.]
            lepton_phi=[-99.,-99.,-99.]
            lepton_eta=[-99.,-99.,-99.]
            lepton_mass=[-99.,-99.,-99.]
            lepton_real=[False,False,False]
            lepton_mishits=[0,0,0]
            lepton_tkIsoId=[0,0,0]
            lepton_softmu=[False,False,False]
        else:
            lepton_idx=[-99,-99]
            lepton_pdg_id=[-99,-99]
            lepton_tight=[False,False]
            lepton_fakeable=[False,False]
            lepton_pt=[-99.,-99.]
            lepton_phi=[-99.,-99.]
            lepton_eta=[-99.,-99.]
            lepton_mass=[-99.,-99.]
            lepton_real=[False,False]
            lepton_mishits=[0,0]
            lepton_tkIsoId=[0,0]
            lepton_softmu=[False,False]
        # store leptons information
        # loose leptons
        for i in range(0,len(loose_leptons)):
            if i >= self.maxObjects:
                break
            lepton_idx[i] = loose_leptons[i]
            if abs(leptons[loose_leptons[i]][0].pdgId) == 13:
                PID = 13
                lepton_tkIsoId[i] = leptons[loose_leptons[i]][0].tkIsoId
                lepton_softmu[i] = leptons[loose_leptons[i]][0].softId
            elif abs(leptons[loose_leptons[i]][0].pdgId) == 11:
                PID = 11
                lepton_mishits[i] = leptons[loose_leptons[i]][0].lostHits

            lepton_pdg_id[i] = leptons[loose_leptons[i]][0].pdgId
            lepton_tight[i] = is_tight[i]
            lepton_fakeable[i] = is_fakeable[i]
            lepton_pt[i] = leptons[loose_leptons[i]][0].pt
            lepton_phi[i] = leptons[loose_leptons[i]][0].phi
            lepton_eta[i] = leptons[loose_leptons[i]][0].eta
            lepton_mass[i] = leptons[loose_leptons[i]][0].mass

            try:
                for j in range(0,len(genparts)):
                    if genparts[j].pt > 5 and abs(genparts[j].pdgId) == PID and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(leptons[loose_leptons[i]][0].eta,leptons[loose_leptons[i]][0].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                        lepton_real[i] = 1
            except:
                pass
        # store jets information
        jet_idx=[-99,-99,-99]
        jet_id=[-99,-99,-99]
        jet_pt=[-99.,-99.,-99.]
        jet_eta=[-99.,-99.,-99.]
        jet_phi=[-99.,-99.,-99.]
        jet_mass=[-99.,-99.,-99.]
        jet_btagCSVV2=[-99.,-99.,-99.]

        for i in range(0,len(loose_jets)):
            if i < 3:
                jet_idx[i]=loose_jets[i]
                jet_id[i]=jets[loose_jets[i]].jetId
                jet_pt[i]=jets[loose_jets[i]].pt
                jet_eta[i]=jets[loose_jets[i]].eta
                jet_phi[i]=jets[loose_jets[i]].phi
                jet_mass[i]=jets[loose_jets[i]].mass
                jet_btagCSVV2[i]=jets[loose_jets[i]].btagCSVV2
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

        self.out.fillBranch("tauVeto",tauVeto)
        self.out.fillBranch("n_tight_leptons",n_tight_leptons)
        self.out.fillBranch("n_fakeable_leptons",n_fakeable_leptons)
        self.out.fillBranch("n_loose_leptons",n_loose_leptons)
        self.out.fillBranch("lepton_idx",lepton_idx)
        self.out.fillBranch("lepton_pdg_id",lepton_pdg_id)
        self.out.fillBranch("lepton_tight",lepton_tight)
        self.out.fillBranch("lepton_fakeable",lepton_fakeable)
        self.out.fillBranch("lepton_pt",lepton_pt)
        self.out.fillBranch("lepton_eta",lepton_eta)
        self.out.fillBranch("lepton_phi",lepton_phi)
        self.out.fillBranch("lepton_mass",lepton_mass)
        self.out.fillBranch("lepton_real",lepton_real)
        self.out.fillBranch("lepton_mishits",lepton_mishits)
        self.out.fillBranch("lepton_tkIsoId",lepton_tkIsoId)
        self.out.fillBranch("lepton_softmu",lepton_softmu)
        # leptons - mll
        mll = -99.
        if lepton_pt[0] > -98. and lepton_pt[1] > -98.:
            mll=(leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[1]][0].p4()).M()
        self.out.fillBranch("mll",mll)

        self.out.fillBranch("bveto",bveto)
        self.out.fillBranch("n_loose_jets",n_loose_jets)
        self.out.fillBranch("jet_idx",jet_idx)
        self.out.fillBranch("jet_id",jet_id)
        self.out.fillBranch("jet_pt",jet_pt)
        self.out.fillBranch("jet_eta",jet_eta)
        self.out.fillBranch("jet_phi",jet_phi)
        self.out.fillBranch("jet_mass",jet_mass)
        self.out.fillBranch("jet_btagCSVV2",jet_btagCSVV2)

        mjj=[-99.,-99.,-99.]
        # jets - mjj : 0 1 2 : mjj mjj02 mjj12
        if jet_pt[0] > -98. and jet_pt[1] > -98.:
            mjj[0]=(jets[loose_jets[0]].p4() + jets[loose_jets[1]].p4()).M()
        if jet_pt[0] > -98. and jet_pt[2] > -98.:
            mjj[1]=(jets[loose_jets[0]].p4() + jets[loose_jets[2]].p4()).M()
        if jet_pt[1] > -98. and jet_pt[2] > -98.:
            mjj[2]=(jets[loose_jets[1]].p4() + jets[loose_jets[2]].p4()).M()
        self.out.fillBranch("mjj",mjj)

        detajj=[-99.,-99.,-99.]
        # jets - detajj : 0 1 2 : detajj detajj02 detajj12
        if jet_pt[0] > -98. and jet_pt[1] > -98.:
            detajj[0]=abs(jets[loose_jets[0]].eta - jets[loose_jets[1]].eta)
        if jet_pt[0] > -98. and jet_pt[2] > -98.:
            detajj[1]=abs(jets[loose_jets[0]].eta + jets[loose_jets[2]].eta)
        if jet_pt[1] > -98. and jet_pt[2] > -98.:
            detajj[2]=abs(jets[loose_jets[1]].eta + jets[loose_jets[2]].eta)
        self.out.fillBranch("detajj",detajj)

        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("met_phi",event.MET_phi)
        # mt: first lepton mt
        mt = -99.
        if lepton_pt[0] > -98.:
            self.out.fillBranch("mt",sqrt(2*leptons[loose_leptons[0]][0].pt * event.MET_pt * (1 - cos(event.MET_phi - leptons[loose_leptons[0]][0].phi))))

        #  mt2: two leptons mt
        mt2 = -99.
        if lepton_pt[0] > -98. and lepton_pt[1] > -98.:
            self.out.fillBranch("mt2",sqrt(2*(leptons[loose_leptons[0]][0].p4()+leptons[loose_leptons[1]][0].p4()).Pt()*event.MET_pt*(1 - cos(event.MET_phi - (leptons[loose_leptons[0]][0].p4()+leptons[loose_leptons[1]][0].p4()).Phi()))))

        self.out.fillBranch("puppimet",event.PuppiMET_pt)
        self.out.fillBranch("puppimet_phi",event.PuppiMET_phi)

        return True

sswwModule = lambda : sswwProducer(minObjects=1,maxObjects=2)
sswwModuleData = lambda : sswwProducer(minObjects=1,maxObjects=2,isData = True)
sswwModule_WZ = lambda : sswwProducer(minObjects=3,maxObjects=3,isWZ = True)
sswwModuleData_WZ = lambda : sswwProducer(minObjects=3,maxObjects=3,isData = True,isWZ = True)
