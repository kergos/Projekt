from src.functions import *


# dirpath = '../../Batchelor-Arbeit/Messdaten/T27C/'  # path to comparedevices
multipledirpath1 = "../../Batchelor-Arbeit/Messdaten/"  # path to comparedevices
multipledirpath2 = "../../Batchelor-Arbeit/Messdaten2/"  # path to comparedevices

# fileplotfunction("../../Batchelor-Arbeit/Messdaten/T27C/B2/MoS2_encapsulated_DevB2_IdVg_5Vs_Vd05V_27C_-20_20V_dark.crv")
# filesystemplotfunction(multipledirpath1)  # only use when ready Takes on Average 10minutes


# secondfileplotfunction("../../Batchelor-Arbeit/Messdaten2/chip1/g1/dev99/22C/IDVG/ch1_g1_dev99_idvg_ar_Vd5V.txt")
# secondfilesystemplotfunction('../../Batchelor-Arbeit/Messdaten2/') # only use when ready Takes on Average 6minutes


searchstrs = ["-20_20V", "Vd05V", "dark"]
# comparedevices(dirpath, searchstrs)
# comparedevicesinfolder(multipledirpath, searchstrs)


searchstr2 = ["dev99"]
antisearch = ["logfile", "sweep", "PBTI", "NBTI", "IDVD", "hysteresis", "Vd001", "Vd01", "Vd1", "Vd3"]
# secondcomparedevices("../../Batchelor-Arbeit/Messdaten2/", searchstr2, antisearch)
# removed condition that all searchstr must be in path for multiple device handling
secondfit("../../Batchelor-Arbeit/Messdaten2/chip1/g1/", searchstr2, antisearch)
