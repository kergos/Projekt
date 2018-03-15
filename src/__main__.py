from src.functions import *


path = '../../Batchelor-Arbeit/Messdaten/'          # put relative path to  here
# dirpath = '../../Batchelor-Arbeit/Messdaten/T27C/'  # path to comparedevices
multipledirpath = '../../Batchelor-Arbeit/Messdaten/'  # path to comparedevices
searchstrs = ["-20_20V", "Vd05V", "dark"]

# comparedevices(dirpath, searchstrs)
# comparedevicesinfolder(multipledirpath, searchstrs)

# fileplotfunction("../../Batchelor-Arbeit/Messdaten/T27C/B2/MoS2_encapsulated_DevB2_IdVg_5Vs_Vd05V_27C_-20_20V_dark.crv")
# filesystemplotfunction(path)  # only use when ready Takes on Average 10minutes
# secondfileplotfunction("../../Batchelor-Arbeit/Messdaten2/chip1/g1/dev10-13/22C/PBTI/ch1_g1_dev10-13_PBTI_1.txt")

#secondfilesystemplotfunction('../../Batchelor-Arbeit/Messdaten2/') # only use when ready Takes on Average 6minutes

searchstr2 = ["dev99_idvg", "22C", "Vd5V"]
antisearch = ["logfile", "sweep", "baked"]
secondcomparedevices('../../Batchelor-Arbeit/Messdaten2/chip1/', searchstr2, antisearch)
