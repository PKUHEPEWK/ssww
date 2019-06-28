from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'DoubleMuon_Run2018A_2018'
config.General.transferLogs= False
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script_data_fr_2018.sh'
config.JobType.inputFiles = ['crab_script_data_fr_2018.py','ssww_keep_and_drop_2018.txt','ssww_output_branch_selection_2018.txt','haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder  = True
config.section_("Data")
config.Data.inputDataset = '/DoubleMuon/Run2018A-Nano14Dec2018-v1/NANOAOD'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 100
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions18/13TeV/ReReco/Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt'

config.Data.outLFNDirBase ='/store/user/%s/nano_fr_2018_v0' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'DoubleMuon_Run2018A_2018'
config.section_("Site")
config.Site.storageSite = "T2_CN_Beijing"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'
