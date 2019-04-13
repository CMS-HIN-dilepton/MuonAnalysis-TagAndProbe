from CRABClient.UserUtilities import config, getUsernameFromSiteDB
config = config()

config.section_('General')
config.General.requestName = 'TnP_HISingleMuon_v1_PbPb5TeV_2018_ZBoson_Data_20190330'
config.General.workArea = 'crab_projects'
config.General.transferOutputs = True
config.General.transferLogs = False

config.section_('JobType')
config.JobType.pluginName = 'Analysis'
config.JobType.psetName = 'tnp_PbPb_data.py'
config.JobType.maxMemoryMB = 2100
config.JobType.maxJobRuntimeMin = 400

config.section_('Data')
config.Data.inputDataset ='/HISingleMuon/HIRun2018A-PromptReco-v1/AOD'
config.Data.inputDBS = 'global'
config.Data.unitsPerJob = 3
config.Data.splitting = 'LumiBased'
config.Data.lumiMask = '/afs/cern.ch/cms/CAF/CMSCOMM/COMM_DQM/certification/Collisions18/HI/PromptReco/Cert_326381-327564_HI_PromptReco_Collisions18_JSON_HF_and_MuonPhys.txt'
config.Data.runRange = '326381-327564'
config.Data.outLFNDirBase = '/store/group/phys_heavyions/%s/TagAndProbe/PbPb2018/TnP/%s' % (getUsernameFromSiteDB(), config.General.requestName)
config.Data.publication = False
config.Data.outputDatasetTag = config.General.requestName

config.section_('Site')
config.Data.ignoreLocality = True
config.Site.whitelist = ['T1_IT_*','T1_US_*','T2_CH_*','T2_FR_*','T2_US_*']
config.Site.storageSite = 'T2_CH_CERN'