import ROOT

from math import cos, sqrt

ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

from PhysicsTools.NanoAODTools.postprocessing.tools import deltaR
from PhysicsTools.NanoAODTools.postprocessing.tools import deltaPhi

#triggersize=32

class sswwProducer(Module):
    def __init__(self,sortkey = lambda x : x.pt,reverse=True,selector=None,minObjects=None,maxObjects=None, preSel=False,year = 2016):
        self.sortkey = lambda (obj,j,i) : sortkey(obj)
        self.reverse = reverse
        self.selector = [(selector[coll] if coll in selector else (lambda x: True)) for coll in self.input] if selector else None # pass dict([(collection_name,lambda obj : selection(obj)])
        self.minObjects = minObjects # save only the first maxObjects objects passing the selection in the merged collection
        self.maxObjects = maxObjects # save only the first maxObjects objects passing the selection in the merged collection
        self.preSel = preSel
        self.year = year
        pass
    def beginJob(self):
        nLepton=self.maxObjects
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("run",  "i")
        self.out.branch("lumi",  "i")
        self.out.branch("event",  "l")
        self.out.branch("npu",  "I")
        self.out.branch("ntruepu",  "F")
        self.out.branch("npvs","I")
        self.out.branch("gen_weight",  "F")
        self.out.branch("tauVeto","B")
        self.out.branch("n_tight_leptons","I")
        self.out.branch("n_fakeable_leptons","I")
        self.out.branch("n_loose_leptons","I")
        self.out.branch("lepton_idx",  "I", lenVar="nLepton")
        self.out.branch("lepton_pdg_id",  "I", lenVar="nLepton")
        self.out.branch("lepton_tight",  "B", lenVar="nLepton")
        self.out.branch("lepton_fakeable",  "B", lenVar="nLepton")
        self.out.branch("lepton_pt",  "F", lenVar="nLepton")
        self.out.branch("lepton_eta",  "F", lenVar="nLepton")
        self.out.branch("lepton_phi",  "F", lenVar="nLepton")
        self.out.branch("lepton_mass",  "F", lenVar="nLepton")
        self.out.branch("lepton_real",  "B", lenVar="nLepton")
        self.out.branch("lepton_mishits",  "I", lenVar="nLepton")
        self.out.branch("lepton_tkIsoId",  "I", lenVar="nLepton")
        self.out.branch("lepton_softmu",  "B", lenVar="nLepton")
        self.out.branch("lepton_zep",  "F", lenVar="nLepton")
        self.out.branch("mll",  "F")
        self.out.branch("mll02",  "F")
        self.out.branch("mll12",  "F")
        self.out.branch("mlll",  "F")
        self.out.branch("mll_z0",  "F")
        self.out.branch("mll_z1",  "F")
        self.out.branch("mllll",  "F")
        self.out.branch("bveto","I")
        self.out.branch("n_loose_jets","I")
        self.out.branch("detajj","F")
        self.out.branch("jet_idx",  "I", lenVar="nJet")
        self.out.branch("jet_id",  "I", lenVar="nJet")
        self.out.branch("jet_pt",  "F", lenVar="nJet")
        self.out.branch("jet_eta",  "F", lenVar="nJet")
        self.out.branch("jet_phi",  "F", lenVar="nJet")
        self.out.branch("jet_mass",  "F", lenVar="nJet")
        self.out.branch("jet_btagCSVV2",  "F", lenVar="nJet")
        self.out.branch("mjj","F")
        self.out.branch("met",  "F")
        self.out.branch("met_phi",  "F")
        self.out.branch("puppimet",  "F")
        self.out.branch("puppimet_phi",  "F")

    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass

    def muonID(self, leptons, idx,n_fakeable_leptons,n_tight_leptons):

        is_fakeable_id = False
        is_tight_id = False

        if self.year == 2016:
            # fakeable muon
            if leptons[idx][0].tightId and leptons[idx][0].pfRelIso04_all < 0.4 and leptons[idx][0].tkIsoId > 0:
                is_fakeable_id=True
                n_fakeable_leptons+=1

            # tight muon
            if leptons[idx][0].tightId and leptons[idx][0].pfRelIso04_all < 0.15:
                is_tight_id=True
                n_tight_leptons+=1

        elif self.year == 2017:
            # fakeable muon
            if leptons[idx][0].tightId and leptons[idx][0].pfRelIso04_all < 0.4 and leptons[idx][0].tkIsoId > 0:
                is_fakeable_id=True
                n_fakeable_leptons+=1

            # tight muon
            # if leptons[idx][0].mvaId > 2 and leptons[idx][0].miniIsoId > 2:
            if leptons[idx][0].tightId and leptons[idx][0].miniIsoId > 2:
                is_tight_id=True
                n_tight_leptons+=1

        elif self.year == 2018:
            # fakeable muon
            if leptons[idx][0].tightId and leptons[idx][0].pfRelIso04_all < 0.4 and leptons[idx][0].tkIsoId > 0:
                is_fakeable_id=True
                n_fakeable_leptons+=1

            # tight muon
            if leptons[idx][0].tightId and leptons[idx][0].miniIsoId > 2:
                is_tight_id=True
                n_tight_leptons+=1

        return is_fakeable_id,is_tight_id,n_fakeable_leptons,n_tight_leptons

    def electronID(self, leptons, idx,n_fakeable_leptons,n_tight_leptons):

        is_fakeable_id = False
        is_tight_id = False

        if self.year == 2016:
            # fakeable electron
            if leptons[idx][0].cutBased_HLTPreSel==1:
                is_fakeable_id=True
                n_fakeable_leptons+=1

            # tight electron
            # if (leptons[idx][0].mvaFall17V1Iso_WP80 and leptons[i][0].tightCharge == 2):
            if (leptons[idx][0].cutBased > 3 and leptons[idx][0].tightCharge == 2):
                is_tight_id=True
                n_tight_leptons+=1

        elif self.year == 2017:
            # fakeable electron
            if abs(leptons[idx][0].eta) <= 1.479 or (abs(leptons[idx][0].eta)>1.479 and leptons[idx][0].sieie < 0.03 and leptons[idx][0].eInvMinusPInv < 0.014):
                is_fakeable_id=True
                n_fakeable_leptons+=1

            # tight electron
            if (leptons[idx][0].cutBased > 3 and leptons[idx][0].tightCharge == 2):
                is_tight_id=True
                n_tight_leptons+=1

        elif self.year == 2018:
            # fakeable electron
            if abs(leptons[idx][0].eta) <= 1.479 or (abs(leptons[idx][0].eta)>1.479 and leptons[idx][0].sieie < 0.03 and leptons[idx][0].eInvMinusPInv < 0.014):
                is_fakeable_id=True
                n_fakeable_leptons+=1

            # tight electron
            # if (leptons[idx][0].mvaFall17V1Iso_WP80 and leptons[i][0].tightCharge == 2):
            if (leptons[idx][0].cutBased > 3 and leptons[idx][0].tightCharge == 2):
                is_tight_id=True
                n_tight_leptons+=1

        return is_fakeable_id,is_tight_id,n_fakeable_leptons,n_tight_leptons

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

        n_loose_leptons = 0
        n_fakeable_leptons = 0
        n_tight_leptons = 0

        if len(leptons) < self.minObjects:
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
                if len(loose_leptons) > self.maxObjects:
                    return False
                is_fakeable_id,is_tight_id,n_fakeable_leptons,n_tight_leptons= self.muonID(leptons, i,n_fakeable_leptons,n_tight_leptons)
                is_fakeable.append(is_fakeable_id)
                is_tight.append(is_tight_id)

            elif abs(leptons[i][0].pdgId) == 11:
                if leptons[i][0].pt < 10:
                    continue
                if abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) > 2.5:
                    continue
                if (abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) <= 1.479 and abs(leptons[i][0].dz) < 0.1 and abs(leptons[i][0].dxy) < 0.05) or (abs(leptons[i][0].eta + leptons[i][0].deltaEtaSC) > 1.479 and abs(leptons[i][0].dz) < 0.2 and abs(leptons[i][0].dxy) < 0.1):
                    # loose electron
                    if leptons[i][0].cutBased >= 1:
                        n_loose_leptons+=1
                        loose_leptons.append(i)
                        if len(loose_leptons) > self.maxObjects:
                            return False
                        is_fakeable_id,is_tight_id,n_fakeable_leptons,n_tight_leptons= self.electronID(leptons, i,n_fakeable_leptons,n_tight_leptons)
                        is_fakeable.append(is_fakeable_id)
                        is_tight.append(is_tight_id)

        if len(loose_leptons) > self.maxObjects or len(loose_leptons) < self.minObjects:
            return False
        # if (n_tight_leptons + n_fakeable_leptons) < 2:
        #    return False
        if self.preSel:
            if leptons[0][0].pt<20 or leptons[1][0].pt<15:
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

                if (is_fakeable[j]== True or is_tight[j] == True) and deltaR(leptons[loose_leptons[j]][0].eta,leptons[loose_leptons[j]][0].phi,jets[i].eta,jets[i].phi) < 0.5:

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

        lepton_idx=[]
        lepton_pdg_id=[]
        lepton_tight=[]
        lepton_fakeable=[]
        lepton_pt=[]
        lepton_phi=[]
        lepton_eta=[]
        lepton_mass=[]
        lepton_real=[]
        lepton_mishits=[]
        lepton_tkIsoId=[]
        lepton_softmu=[]
        lepton_zep=[]

        detajj=jets[loose_jets[0]].eta - jets[loose_jets[1]].eta

        mjj=(jets[loose_jets[0]].p4() + jets[loose_jets[1]].p4()).M()
        if self.preSel:
            if mjj<500:
                return False

        # store leptons information
        # loose leptons
        for i in range(0,len(loose_leptons)):
            if i >= self.maxObjects:
                break
            lepton_idx.append(loose_leptons[i])
            if abs(leptons[loose_leptons[i]][0].pdgId) == 13:
                PID = 13
                lepton_tkIsoId.append(leptons[loose_leptons[i]][0].tkIsoId)
                lepton_softmu.append(leptons[loose_leptons[i]][0].softId)
                lepton_mishits.append(-9999)
            elif abs(leptons[loose_leptons[i]][0].pdgId) == 11:
                PID = 11
                lepton_tkIsoId.append(-9999)
                lepton_softmu.append(False)
                lepton_mishits.append(leptons[loose_leptons[i]][0].lostHits)

            lepton_pdg_id.append(leptons[loose_leptons[i]][0].pdgId)
            lepton_tight.append(is_tight[i])
            lepton_fakeable.append(is_fakeable[i])
            lepton_pt.append(leptons[loose_leptons[i]][0].pt)
            lepton_phi.append(leptons[loose_leptons[i]][0].phi)
            lepton_eta.append(leptons[loose_leptons[i]][0].eta)
            lepton_mass.append(leptons[loose_leptons[i]][0].mass)
            lepton_zep.append(abs((leptons[loose_leptons[i]][0].eta-(jets[loose_jets[0]].eta + jets[loose_jets[1]].eta)/2.)/detajj))
            try:
                for j in range(0,len(genparts)):
                    if genparts[j].pt > 5 and abs(genparts[j].pdgId) == PID and ((genparts[j].statusFlags & isprompt_mask == isprompt_mask) or (genparts[j].statusFlags & isdirectprompttaudecayproduct_mask == isdirectprompttaudecayproduct_mask)) and deltaR(leptons[loose_leptons[i]][0].eta,leptons[loose_leptons[i]][0].phi,genparts[j].eta,genparts[j].phi) < 0.3:
                        lepton_real.append(True)
                    else:
                        lepton_real.append(False)
            except:
                pass
        # store jets information
        jet_idx=[]
        jet_id=[]
        jet_pt=[]
        jet_eta=[]
        jet_phi=[]
        jet_mass=[]
        jet_btagCSVV2=[]

        for i in range(0,len(loose_jets)):
            if i < 3:
                jet_idx.append(loose_jets[i])
                jet_id.append(jets[loose_jets[i]].jetId)
                jet_pt.append(jets[loose_jets[i]].pt)
                jet_eta.append(jets[loose_jets[i]].eta)
                jet_phi.append(jets[loose_jets[i]].phi)
                jet_mass.append(jets[loose_jets[i]].mass)
                jet_btagCSVV2.append(jets[loose_jets[i]].btagCSVV2)
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
        self.out.fillBranch("lepton_zep",lepton_zep)
        mll = -9999.
        if len(loose_leptons)>1:
            mll=(leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[1]][0].p4()).M()
        self.out.fillBranch("mll",mll)
        mll02=-9999.
        mll12=-9999.
        mlll=-9999.
        if len(loose_leptons)>2:
            mll02=(leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[2]][0].p4()).M()
            mll12=(leptons[loose_leptons[1]][0].p4() + leptons[loose_leptons[2]][0].p4()).M()
            mlll=(leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[1]][0].p4() + leptons[loose_leptons[2]][0].p4()).M()
        self.out.fillBranch("mll02",mll02)
        self.out.fillBranch("mll12",mll12)
        self.out.fillBranch("mlll",mlll)
        mll_z0=-9999.
        mll_z1=-9999.
        mllll=-9999.
        tmp2 = -9999.
        if len(loose_leptons)>3:
            for i in range(1,len(loose_leptons)):
                tmp=(leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[i]][0].p4()).M()-91.2
                if abs(tmp)<abs(tmp2):
                    mll_z0 = (leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[i]][0].p4()).M()
                    tmp2 = tmp
                    remain_lepton=[1,2,3]
                    remain_lepton.remove(i)
                    mll_z1 = (leptons[loose_leptons[remain_lepton[0]]][0].p4() + leptons[loose_leptons[remain_lepton[1]]][0].p4()).M()
            mllll=(leptons[loose_leptons[0]][0].p4() + leptons[loose_leptons[1]][0].p4() + leptons[loose_leptons[2]][0].p4() + leptons[loose_leptons[3]][0].p4()).M()
        self.out.fillBranch("mll_z0",mll_z0)
        self.out.fillBranch("mll_z1",mll_z1)
        self.out.fillBranch("mllll",mllll)
        self.out.fillBranch("bveto",bveto)
        self.out.fillBranch("n_loose_jets",n_loose_jets)
        self.out.fillBranch("detajj",detajj)
        self.out.fillBranch("jet_idx",jet_idx)
        self.out.fillBranch("jet_id",jet_id)
        self.out.fillBranch("jet_pt",jet_pt)
        self.out.fillBranch("jet_eta",jet_eta)
        self.out.fillBranch("jet_phi",jet_phi)
        self.out.fillBranch("jet_mass",jet_mass)
        self.out.fillBranch("jet_btagCSVV2",jet_btagCSVV2)
        self.out.fillBranch("mjj",mjj)
        self.out.fillBranch("met",event.MET_pt)
        self.out.fillBranch("met_phi",event.MET_phi)
        self.out.fillBranch("puppimet",event.PuppiMET_pt)
        self.out.fillBranch("puppimet_phi",event.PuppiMET_phi)


        return True

sswwModule2016 = lambda : sswwProducer(minObjects=2,maxObjects=4,preSel=True,year=2016)
sswwModule2017 = lambda : sswwProducer(minObjects=2,maxObjects=4,preSel=True,year=2017)
sswwModule2018 = lambda : sswwProducer(minObjects=2,maxObjects=4,preSel=True,year=2018)
sswwModule_fr_2016 = lambda : sswwProducer(minObjects=1,maxObjects=1,preSel=True,year=2016)
sswwModule_fr_2017 = lambda : sswwProducer(minObjects=1,maxObjects=1,preSel=True,year=2017)
sswwModule_fr_2018 = lambda : sswwProducer(minObjects=1,maxObjects=1,preSel=True,year=2018)
