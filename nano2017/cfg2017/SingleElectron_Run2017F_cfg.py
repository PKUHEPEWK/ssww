from WMCore.Configuration import Configuration
from CRABClient.UserUtilities import config, getUsernameFromSiteDB

config = Configuration()

config.section_("General")
config.General.requestName = 'SingleElectron_Run2017F_2017'
config.General.transferLogs= False
config.section_("JobType")
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'PSet.py'
config.JobType.scriptExe = 'crab_script.sh'
config.JobType.inputFiles = ['crab_data_script.py','ssww_keep_and_drop.txt','ssww_output_branch_selection.txt','haddnano.py'] #hadd nano will not be needed once nano tools are in cmssw
config.JobType.sendPythonFolder  = True
config.section_("Data")
config.Data.inputDataset = '/SingleElectron/Run2017F-Nano14Dec2018-v1/NANOAOD'
#config.Data.inputDBS = 'phys03'
config.Data.inputDBS = 'global'
config.Data.splitting = 'LumiBased'
#config.Data.splitting = 'EventAwareLumiBased'
config.Data.unitsPerJob = 60
config.Data.lumiMask = 'https://cms-service-dqm.web.cern.ch/cms-service-dqm/CAF/certification/Collisions17/13TeV/ReReco/Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt'

config.Data.outLFNDirBase ='/store/user/%s/nano2017' % (getUsernameFromSiteDB())
config.Data.publication = False
config.Data.outputDatasetTag = 'SingleElectron_Run2017F_2017'
config.section_("Site")
config.Site.storageSite = "T2_CN_Beijing"

#config.Site.storageSite = "T2_CH_CERN"
#config.section_("User")
#config.User.voGroup = 'dcms'
