
N_GEN = 100000

#------------------------------
#         Cs   Co   Eu   bkg.
#------------------------------
FRACT = [ 30., 50., 10., 10.]
#------------------------------

PATH_TO_FILES = "../../spectra/sources/"

FNAMES = [ "Cs-137/Cs-137_atDet.xml",
           "Co-60/Co-60_atDet.xml"  ,
           "Eu-152/Eu-152_atDet.xml",
           "bkg.xml"]

#===============================================================================
sum_F = 0.
for ff in FRACT:
    sum_F += ff

F_i = []
for ff in FRACT:
    F_i.append( ff/sum_F )

#===============================================================================

import ostap.fitting.models as Models
from ostap.histos.graphs    import makeGraph
from  math import log, exp, pow

def get_tag( file , tag):
    for line in file:
        if ("<"+tag+">") in line:
            return line[:-1].split("<"+tag+">")[1].split("</"+tag+">")[0]

def get_data(file):
    data = []
    tag = "DataPoint"
    for line in file:
        if ("<"+tag+">") in line:
            data.append( int ( line[:-1].split("<"+tag+">")[1].split("</"+tag+">")[0] ) )
    return data

dat_l   = []
t_start = []
t_end   = []
t_dur   = []
t_live  = []

for FNAME in FNAMES:
    with open(PATH_TO_FILES+FNAME,"r") as fl:
        t_start.append(         get_tag(fl,"StartTime"      )   )
        t_end  .append(         get_tag(fl,"EndTime"        )   )
        t_dur  .append(  float( get_tag(fl,"MeasurementTime") ) )
        t_live .append(  float( get_tag(fl,"LiveTime"       ) ) )
        dat_l.append( get_data(fl) )


h_Cs = ROOT.TH1F("h_Cs","Signal (Cs)", 1024,  0.5, 1024.5 )
h_Co = ROOT.TH1F("h_Co","Signal (Co)", 1024,  0.5, 1024.5 )
h_Eu = ROOT.TH1F("h_Eu","Signal (Eu)", 1024,  0.5, 1024.5 )
h_bkg= ROOT.TH1F("h_bkg","Background", 1024,  0.5, 1024.5 )

for ch in range(len(dat_l[0])):
    h_Cs[ch+1] = VE(dat_l[0][ch],dat_l[0][ch])

for ch in range(len(dat_l[1])):
    h_Co[ch+1] = VE(dat_l[1][ch],dat_l[1][ch])

for ch in range(len(dat_l[2])):
    h_Eu[ch+1] = VE(dat_l[2][ch],dat_l[2][ch])

for ch in range(len(dat_l[3])):
    h_bkg[ch+1] = VE(dat_l[3][ch],dat_l[3][ch])

h_Cs.SetLineColor(2)
h_Co.SetLineColor(4)
h_Eu.SetLineColor(8)

h_bkg.SetLineWidth(2)
h_Cs.SetLineWidth(2)
h_Co.SetLineWidth(2)
h_Eu.SetLineWidth(2)

#h_Cs .Scale( 1. / h_Cs .Integral() )
#h_Co .Scale( 1. / h_Co .Integral() )
#h_Eu .Scale( 1. / h_Eu .Integral() )
#h_bkg.Scale( 1. / h_bkg.Integral() )

#h_Eu.Draw("hist")
#h_Cs.Draw("same hist")
#h_Co.Draw("same hist")
#h_bkg.Draw("same hist")

h_gen= ROOT.TH1F("h_gen","Generated spectrum", 1024,  0.5, 1024.5 )

hh = [h_Cs, h_Co, h_Eu, h_bkg]

for idx in range(len(hh)):
    for e in range( int( N_GEN*F_i[idx] ) ):
        h_gen.Fill( hh[idx].GetRandom() )

h_gen.Draw("hist")

ch = ROOT.RooRealVar("ch","ch",0.5,1024.5)
sig_Cs = Models.Histo1D_pdf("Cs" ,h_Cs ,xvar=ch )
sig_Co = Models.Histo1D_pdf("Co" ,h_Co ,xvar=ch )
sig_Eu = Models.Histo1D_pdf("Eu" ,h_Eu ,xvar=ch )
bkg    = Models.Histo1D_pdf("bkg",h_bkg,xvar=ch )

model  = Models.Fit1D( signal = sig_Cs                 ,
                       background = bkg                ,
                       othersignals = [sig_Co, sig_Eu] )
#                       extended = False)


r,w = model.fitHisto( h_gen, draw=True, silent=True )

print("\n\n")
print(r)
print("\n\n\n")
print( "Cs-137     : ", r("S_0")[0]*100./N_GEN, " %  <-- ( real = ", int(F_i[0]*100.)," %)",sep = "" )
print( "Co-60      : ", r("S_1")[0]*100./N_GEN, " %  <-- ( real = ", int(F_i[1]*100.)," %)",sep = "" )
print( "Eu-152     : ", r("S_2")[0]*100./N_GEN, " %  <-- ( real = ", int(F_i[2]*100.)," %)",sep = "" )
print( "Background : ", r("B"  )[0]*100./N_GEN, " %  <-- ( real = ", int(F_i[3]*100.)," %)",sep = "" )
print("\n\n")
