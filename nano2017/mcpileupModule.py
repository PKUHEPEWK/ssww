import ROOT
ROOT.PyConfig.IgnoreCommandLineOptions = True

from PhysicsTools.NanoAODTools.postprocessing.framework.datamodel import Collection
from PhysicsTools.NanoAODTools.postprocessing.framework.eventloop import Module

class mcpileupProducer(Module):
    def __init__(self):
        pass
    def beginJob(self):
        pass
    def endJob(self):
        pass
    def beginFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        self.out = wrappedOutputTree
        self.out.branch("npu",  "I");
        self.out.branch("ntruepu",  "F");
    def endFile(self, inputFile, outputFile, inputTree, wrappedOutputTree):
        pass
    def analyze(self, event):
        """process event, return True (go to next module) or False (fail, go to next event)"""
        if hasattr(event,'Pileup_nPU'):
            self.out.fillBranch("npu",event.Pileup_nPU)
        else:
            self.out.fillBranch("npu",0)

        if hasattr(event,'Pileup_nTrueInt'):
            self.out.fillBranch("ntruepu",event.Pileup_nTrueInt)
        else:
            self.out.fillBranch("ntruepu",0)
        return True


# define modules using the syntax 'name = lambda : constructor' to avoid having them loaded when not needed

mcpileupModuleConstr = lambda : mcpileupProducer()
