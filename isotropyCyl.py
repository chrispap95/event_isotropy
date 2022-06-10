import ROOT
import src.eventIsotropy as iso
import numpy as np
from DataFormats.FWLite import Events, Handle
import time
import sys
import argparse

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
options = parser.parse_args()

events = Events ([options.filename])

handleGen  = Handle ("std::vector<reco::GenParticle>")
labelGen = ("genParticles", "", "GEN")

handlexyz0 = Handle("ROOT::Math::PositionVector3D<ROOT::Math::Cartesian3D<float>,ROOT::Math::DefaultCoordinateSystemTag>")
labelxyz0 = ("genParticles","xyz0")

handlet0 = Handle("float")
labelt0 = ("genParticles","t0")

# Open output file
fileOut = ROOT.TFile(options.output,"RECREATE")

# Define histograms
h1 = ROOT.TH1F("mult","multiplicity;nTracks",200,0,1000)
h2 = ROOT.TH1F("iso1","isotropy;isotropy",100,0,1)

# Define granularity of uniform distribution
N = options.N

# loop over events
time0 = time.time()
count = 0
for event in events:
    if(count%1000==0): print("Processing event %d"%count)
    count+=1
    if count==options.nMax: break

    event.getByLabel (labelGen, handleGen)
    event.getByLabel (labelxyz0, handlexyz0)
    event.getByLabel (labelt0, handlet0)

    # get the product
    t0 = handlet0.product()
    v0 = handlexyz0.product()
    genPart = handleGen.product()


    nTracks = 0
    genPTtrks = np.array([])
    genPhitrks = np.array([])
    genEtatrks = np.array([])
    for i in range(len(genPart)):
        if genPart[i].status() == 1 and abs(genPart[i].eta()) < 2.5 and genPart[i].pt() > 1:
            if abs(genPart[i].charge()) > 0:
                nTracks+=1
                genPTtrks = np.append(genPTtrks, genPart[i].pt())
                genPhitrks = np.append(genPhitrks, genPart[i].phi())
                genEtatrks = np.append(genEtatrks, genPart[i].eta())

    # Generate uniform distribution
    cylPointsUni = iso.cylGen.cylinderGen(N,2.5)
    cylPTuni = np.full(len(cylPointsUni), 1.) 
    cylPoints1 = np.column_stack((genEtatrks,genPhitrks))
    cylPT1 = genPTtrks


    M1 = iso.emdVar._cdist_phi_y(cylPointsUni, cylPoints1, 2.5)
    emdval1 = iso.emdVar.emd_Calc(cylPTuni, cylPT1, M1)

    h1.Fill(nTracks)
    h2.Fill(emdval1)

print("This code took %f sec"%(time.time()-time0))
print("mean = %f, std=%f"%(h2.GetMean(),h2.GetStdDev()))
fileOut.Write()
fileOut.Close()
