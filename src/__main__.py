from src.functions import *


path = '../../Batchelor-Arbeit/Messdaten/'          # put relative path to  here
dirpath = '../../Batchelor-Arbeit/Messdaten/T27C/'  # path to comparedevices
multipledirpath = '../../Batchelor-Arbeit/Messdaten/'  # path to comparedevices
searchstrs = ["-20_20V", "Vd05V", "dark"]

# comparedevices(dirpath, searchstrs)
comparedevicesinfolder(multipledirpath, searchstrs)

# fileplotfunction("../../Batchelor-Arbeit/Messdaten/T27C/B2/MoS2_encapsulated_DevB2_IdVg_5Vs_Vd05V_27C_-20_20V_dark.crv")
# filesystemplotfunction(path) #only use when ready Takes on Average 10minutes



