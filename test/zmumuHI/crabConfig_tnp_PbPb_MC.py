from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.section_('General')
config.General.requestName = 'TnP_HISingleMuon_PbPb5TeV_2018_ZBoson_MC_20190331'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'tnp_PbPb_MC.py'
config.JobType.maxMemoryMB = 2400
config.JobType.maxJobRuntimeMin = 150

config.section_('Data')
config.Data.inputDataset ='/ZMM_5p02TeV_TuneCP5_Embd/anstahll-ZMM_5p02TeV_TuneCP5_Embd_RECO_22032019-5db5dfa073297cb96791f14c622e83e2/USER'
config.Data.inputDBS = 'phys03'
config.Data.unitsPerJob = 4
config.Data.splitting = 'FileBased'
config.Data.outLFNDirBase = '/store/group/phys_heavyions/%s/TagAndProbe/PbPb2018/TnP/%s' % (getUsernameFromSiteDB(), config.General.requestName)
config.Data.publication = False
config.Data.outputDatasetTag = config.General.requestName

config.section_('Site')
config.Data.ignoreLocality = True
config.Site.whitelist = ['T1_FR_*','T2_CH_*','T2_FR_*','T2_US_*']
config.Site.storageSite = 'T2_CH_CERN'