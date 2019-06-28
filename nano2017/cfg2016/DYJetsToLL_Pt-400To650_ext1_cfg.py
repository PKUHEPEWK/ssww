from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'DYJetsToLL_Pt-400To650_ext1_2016'
config.General.transferLogs= False
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_2016.sh'
config.JobType.inputFiles = ['crab_script_2016.py','ssww_keep_and_drop_2016.txt','ssww_output_branch_selection_2016.txt','haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder  = True
config.section_("Data")
config.Data.inputDataset = '/DYJetsToLL_Pt-400To650_TuneCUETP8M1_13TeV-amcatnloFXFX-pythia8/RunIISummer16NanoAODv4-PUMoriond17_Nano14Dec2018_102X_mcRun2_asymptotic_v6_ext1-v2/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 20
config.Data.totalUnits = -1

config.Data.outLFNDirBase ='/store/user/%s/nano2016_v0' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'DYJetsToLL_Pt-400To650_ext1_2016'
config.section_("Site")
config.Site.storageSite = "T2_CN_Beijing"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'
