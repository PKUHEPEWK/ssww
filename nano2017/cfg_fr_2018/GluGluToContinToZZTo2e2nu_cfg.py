from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'GluGluToContinToZZTo2e2nu_2018'
config.General.transferLogs= False
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_fr_2018.sh'
config.JobType.inputFiles = ['crab_script_fr_2018.py','ssww_keep_and_drop_2018.txt','ssww_output_branch_selection_2018.txt','haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder  = True
config.section_("Data")
config.Data.inputDataset = '/GluGluToContinToZZTo2e2nu_13TeV_MCFM701_pythia8/RunIIAutumn18NanoAODv4-Nano14Dec2018_102X_upgrade2018_realistic_v16-v1/NANOAODSIM'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'FileBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 20
config.Data.totalUnits = -1

config.Data.outLFNDirBase ='/store/user/%s/nano_fr_2018_v0' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'GluGluToContinToZZTo2e2nu_2018'
config.section_("Site")
config.Site.storageSite = "T2_CN_Beijing"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'
