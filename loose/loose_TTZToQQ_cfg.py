from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'loose_TTZToQQ'
config.General.transferLogs= True
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_loose_script.py','ssww_keep_and_drop.txt','ssww_output_branch_selection.txt','haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder  = True
config.section_("Data")
config.Data.inputDataset = '/TTZToQQ_TuneCUETP8M1_13TeV-amcatnlo-pythia8/RunIISummer16NanoAODv4-PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 20
config.Data.totalUnits = -1

config.Data.outLFNDirBase = '/store/user/%s/nano2016' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'loose_TTZToQQ'
config.section_("Site")
config.Site.storageSite = "T2_CH_CERNBOX"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'
