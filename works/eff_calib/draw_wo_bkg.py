import ostap.fitting.models as Models
from ostap.histos.graphs    import makeGraph
from  math import log, exp, pow

PATH_TO_FILES = "../../spectra/sources/"

FNAMES = [ "Cs-137/Cs-137_148mm.xml", "bkg.xml"]

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


h_sig= ROOT.TH1F("h_sig","Signal"    , 1024,  0.5, 1024.5 )
h_bkg= ROOT.TH1F("h_bkg","Background", 1024,  0.5, 1024.5 )

for ch in range(len(dat_l[0])):
    h_sig[ch+1] = VE(dat_l[0][ch],dat_l[0][ch])

for ch in range(len(dat_l[1])):
    h_bkg[ch+1] = VE(dat_l[1][ch],dat_l[1][ch])*( t_live[0] / t_live[1] )

h_sub = h_sig - h_bkg
h_sub.Draw()

h_sig.red()

