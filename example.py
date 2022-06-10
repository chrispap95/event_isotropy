import numpy as np
import src.eventIsotropy as iso
import ROOT

N = 16

ringPoints1 = iso.cylGen.ringGen(N)
ringPT1 = np.full(len(ringPoints1), 1.)
ringPT2 = ringPT1

c1 = ROOT.TCanvas("c1","c1",1)
h1 = ROOT.TH1F("h1","isotropy",50,0,1)

emdSpec = []
for i in range(1000):
    ringPoints2 = iso.cylGen.ringGenShift(N)
    M = iso.emdVar._cdist_phicos(ringPoints1,ringPoints2)
    emdval = iso.emdVar.emd_Calc(ringPT1, ringPT2, M)
    emdSpec.append(emdval)
    h1.Fill(emdval)

h1.Draw()
