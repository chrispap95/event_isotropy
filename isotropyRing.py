import ROOT
import src.eventIsotropy as iso
import numpy as np
from DataFormats.FWLite import Events, Handle
import time
import sys
import argparse
from array import array

parser = argparse.ArgumentParser(description="Calculates iso")
parser.add_argument("-f", "--file", dest="filename",
                  help="full path to file to process")
parser.add_argument("-o", "--output", dest="output",
                  help="local path for output file")
parser.add_argument("-N", "--segmentation",
                  action="store", dest="N", type=int, default=64,
                  help="ring segmentation")
parser.add_argument("-M", "--nMax",
                  action="store", dest="nMax", type=int, default=sys.maxsize,
                  help="max events to process. Default is all.")
parser.add_argument("-P", "--ptcut",
                  action="store", dest="ptcut", type=int, default=0,
                  help="sum pt cut")
options = parser.parse_args()

events = Events ([options.filename])

handleGen  = Handle ("std::vector<reco::GenParticle>")
labelGen = ("genParticles", "", "GEN")

# Open output file
fileOut = ROOT.TFile(options.output,"RECREATE")

# Define histograms
h1 = ROOT.TH1F("mult","multiplicity;nTracks",200,0,1000)
h2 = ROOT.TH1F("iso1","isotropy;isotropy",100,0,1)
tree = ROOT.TTree("tree","output tree")
nTracks = array('d', [0])
isotropy = array('d', [0])
tree.Branch('nTracks', nTracks, 'nTracks/D')
tree.Branch('isotropy', isotropy, 'iso/D')

# Define granularity of uniform distribution
N = options.N

# Sum PT cut
ptcut = options.ptcut

# loop over events
time0 = time.time()
count = 0
for event in events:
    if(count%1000==0): print("Processing event %d"%count)
    count+=1
    if count==options.nMax: break

    event.getByLabel (labelGen, handleGen)

    # get the product
    genPart = handleGen.product()

    nT = 0
    pTsum = 0
    genPTtrks = np.array([])
    genPhitrks = np.array([])
    for i in range(len(genPart)):
        if genPart[i].status() == 1 and abs(genPart[i].eta()) < 2.4 and genPart[i].pt() > 0.1:
            if abs(genPart[i].charge()) > 0:
                nT+=1
                pTsum += genPart[i].pt()
            genPTtrks = np.append(genPTtrks, genPart[i].pt())
            genPhitrks = np.append(genPhitrks, genPart[i].phi())

    if pTsum < ptcut:
        continue

    ringPointsUni = iso.cylGen.ringGen(N)
    ringPTuni = np.full(len(ringPointsUni), 1.) 
    ringPoints1 = genPhitrks
    ringPT1 = genPTtrks

    M1 = iso.emdVar._cdist_phicos(ringPointsUni,ringPoints1)
    emdval1 = iso.emdVar.emd_Calc(ringPTuni, ringPT1, M1)

    h1.Fill(nT)
    h2.Fill(emdval1)
    nTracks[0] = float(nT)
    isotropy[0] = float(emdval1)
    tree.Fill()

print("This code took %f sec"%(time.time()-time0))
print("mean = %f, std=%f"%(h2.GetMean(),h2.GetStdDev()))
fileOut.Write()
fileOut.Close()
