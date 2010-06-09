import FWCore.ParameterSet.Config as cms

### USAGE:
###    cmsRun fitTrigger_ICHEP.py <scenario>
### scenarios:
###   - data_all:    will fit tnpJPsi_Data.root with bins suitable for the current data
###   - datalike_mc: will fit tnpJPsi_{JPsiMuMu,ppMuX}_Spring10_0.117pb.root MC but
###                  with same config as data

import sys
args = sys.argv[1:]
if (sys.argv[0] == "cmsRun"): args =sys.argv[2:]
scenario = "data_all"
if len(args) > 0: scenario = args[0]
print "Will run scenario ", scenario 

process = cms.Process("TagProbe")

process.load('FWCore.MessageService.MessageLogger_cfi')

process.source = cms.Source("EmptySource")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

Template = cms.EDAnalyzer("TagProbeFitTreeAnalyzer",
    NumCPU = cms.uint32(1),
    SaveWorkspace = cms.bool(False),

    Variables = cms.PSet(
        mass   = cms.vstring("Tag-Probe Mass", "2.8", "3.5", "GeV/c^{2}"),
        pt     = cms.vstring("Probe p_{T}", "0", "1000", "GeV/c"),
        abseta = cms.vstring("Probe |#eta|", "0", "2.5", ""),
        tag_pt = cms.vstring("Tag p_{T}", "2.6", "1000", "GeV/c"),
        mcTrue = cms.vstring("MC true", "dummy[true=1,false=0]"),
    ),

    Categories = cms.PSet(
        # Efficiencies to measure
        Mu3 = cms.vstring("Mu3", "dummy[pass=1,fail=0]"),
        # Denominator
        POG_Glb = cms.vstring("POG_Glb", "dummy[pass=1,fail=0]"),
        L1DoubleMuOpen = cms.vstring("L1DoubleMuOpen", "dummy[pass=1,fail=0]"),
        # Other constraints
        tag_Mu3 = cms.vstring("tag_Mu3", "dummy[pass=1,fail=0]"),
    ),

    PDFs = cms.PSet(
        gaussPlusExpo = cms.vstring(
            "Gaussian::signal(mass, mean[3.1,3.0,3.2], sigma[0.05,0.02,0.1])",
            "Exponential::backgroundPass(mass, lp[0,-5,5])",
            "Exponential::backgroundFail(mass, lf[0,-5,5])",
            "efficiency[0.9,0,1]",
            "signalFractionInPassing[0.9]"
        )
    ),

    Efficiencies = cms.PSet(), # will be filled later
)

CONSTRAINTS = cms.PSet(
    tag_Mu3 = cms.vstring("pass"),
    POG_Glb = cms.vstring("pass"),
)
PT_ETA_BINS = cms.PSet(
    CONSTRAINTS,
    pt     = cms.vdouble(  2.0, 3.0, 5.0, 12.0),
    abseta = cms.vdouble(  0.0, 0.8, 1.2, 1.6, 2.4), 
)


process.TnP_Trigger = Template.clone(
    InputFileNames = cms.vstring("tnpJPsi_Data.root"),
    InputDirectoryName = cms.string("histoTrigger"),
    InputTreeName = cms.string("fitter_tree"),
    OutputFileName = cms.string("TnP_ICHEP_Trigger_%s.root" % scenario),
    Efficiencies = cms.PSet(),
)

if scenario == "data_all":
    process.TnP_Trigger.binsForMassPlots = cms.uint32(35)

if scenario == "datalike_mc":
    process.TnP_Trigger.InputFileNames = [
        "tnpJPsi_JPsiMuMu_Spring10_0.117pb.root",
        "tnpJPsi_ppMuX_Spring10_0.117pb.root"
    ]



for T in [ "Mu3", "L1DoubleMuOpen" ]:
    setattr(process.TnP_Trigger.Efficiencies, T+"_pt_abseta", cms.PSet(
        EfficiencyCategoryAndState = cms.vstring(T,"pass"),
        UnbinnedVariables = cms.vstring("mass"),
        BinnedVariables = PT_ETA_BINS,
        BinToPDFmap = cms.vstring("gaussPlusExpo")
    ))
    if scenario == "datalike_mc":
        setattr(process.TnP_Trigger.Efficiencies, T+"_pt_abseta_mcTrue", cms.PSet(
            EfficiencyCategoryAndState = cms.vstring(T,"pass"),
            UnbinnedVariables = cms.vstring("mass"),
            BinnedVariables = PT_ETA_BINS.clone(mcTrue = cms.vstring("true"))
        )) 
    if T != "L1DoubleMuOpen":
        setattr(process.TnP_Trigger.Efficiencies, T+"overL1_pt_abseta", cms.PSet(
            EfficiencyCategoryAndState = cms.vstring(T,"pass"),
            UnbinnedVariables = cms.vstring("mass"),
            BinnedVariables = PT_ETA_BINS.clone(L1DoubleMuOpen = cms.vstring("pass")),
            BinToPDFmap = cms.vstring("gaussPlusExpo")
        ))
        if scenario == "datalike_mc":
            setattr(process.TnP_Trigger.Efficiencies, T+"overL1_pt_abseta_mcTrue", cms.PSet(
                EfficiencyCategoryAndState = cms.vstring(T,"pass"),
                UnbinnedVariables = cms.vstring("mass"),
                BinnedVariables = PT_ETA_BINS.clone(L1DoubleMuOpen = cms.vstring("pass"), mcTrue = cms.vstring("true"))
            )) 

process.p = cms.Path(
    process.TnP_Trigger
)

