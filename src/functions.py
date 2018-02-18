from multiprocessing import Pool
from bisect import *
import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import time


# tutorialfunction
def basicplotfunction():
    print("Start Plotting")

    # Data for plotting
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)

    # Note that using plt.subplots below is equivalent to using
    # fig = plt.figure and then ax = fig.add_subplot(111)
    fig, ax = plt.subplots()
    ax.plot(t, s)

    ax.set(xlabel='time (s)', ylabel='voltage (mV)',
           title='About as simple as it gets, folks')
    ax.grid()

    fig.savefig("../plots/test.png")
    plt.show()


# first Plot from File
def basicfileplotfunction():
    with open("../../Batchelor-Arbeit/Messdaten/T27C/A1/MoS2_encapsulated_DevA1_IdVg_10Vs_Vd1V_27C_-20_20V.crv") as f:
        for i in range(6):      # starting at line 11 where plot data starts
            f.__next__()
        data = f.read()

    data = data.split('\n') #splitting seperate lines
    print(data)
    data = [row.split('  ') for row in data] #removing blanks
    data.pop() #remove last useless Array
    x  = [float(column[1]) for column in data]
    y1 = [float(column[2]) for column in data]
    y2 = [float(column[3]) for column in data]
    y3 = [float(column[4]) for column in data]

    fig, ax = plt.subplots()
    ax.plot(x, y1)
    ax.set(xlabel='Time (s)', ylabel='VBackGate (V)',
           title='T27C-A1_VBackGate')
    ax.grid()
    fig.savefig("../../Batchelor-Arbeit/Plots/T27C/A1_VBackGate.png")

    fig, ax = plt.subplots()

    ax.plot(x, y2)
    ax.set(xlabel='Time (s)', ylabel='VDrain (V)',
           title='T27C-A1_VDrain')
    ax.grid()
    fig.savefig("../../Batchelor-Arbeit/Plots/T27C/A1_VDrain.png")

    fig, ax = plt.subplots()

    ax.plot(x, y3)
    ax.set(xlabel='Time (s)', ylabel='IDrain (I)',
           title='T27C-A1_IDrain')
    ax.grid()
    fig.savefig("../../Batchelor-Arbeit/Plots/T27C/A1_IDrain.png")


# multiple plots from one .crv file and creating
def fileplotfunction(pathtofile):
    if os.path.isfile(pathtofile):
        with open(pathtofile) as f:
            for i in range(6):                    # starting at line 11 where plot data starts
                f.__next__()
            data = f.read()

        data = data.split('\n')                   # splitting seperate lines
        data = [row.split('  ') for row in data]  # removing blanks
        data.pop()                                # remove last useless Array in crv

        x = [float(column[1]) for column in data]   #time
        y1 = [float(column[2]) for column in data]  #VBackGate
        y2 = [float(column[3]) for column in data]  #VDrain
        y3 = [float(column[4]) for column in data]  #IDrain

        # string manipulation for naming purposes very static, needs workaround
        newstring = pathtofile.split('/')
        # print(newstring)
        dirname1 = newstring[4]
        dirname2 = newstring[5]
        filename = newstring[6]

        temppath = "../../Batchelor-Arbeit/Plots/"
        
        if not os.path.exists(os.path.join(temppath, dirname1)):
            os.makedirs(os.path.join(temppath, dirname1))

        temppath = os.path.join(temppath, dirname1)

        if not os.path.exists(os.path.join(temppath, dirname2)):
            os.makedirs(os.path.join(temppath, dirname2))

        temppath = os.path.join(temppath, dirname2)+"/"


        fig, ax = plt.subplots()


        ax.plot(x, y1)
        ax.set(xlabel='Time (s)', ylabel='VBackGate (V)',
               title=filename[:-4] + "__VBackgate")
        ax.grid()
        fig.savefig(temppath+filename[:-4]+"__VBackgate.png")
        plt.close(fig)

        fig, ax = plt.subplots()
        ax.plot(x, y2)
        #ax.set_yscale("log")
        ax.set(xlabel='Time (s)', ylabel='VDrain (V)',
               title=filename[:-4] + "__VDrain\n")
        ax.grid()
        fig.savefig(temppath+filename[:-4]+"__VDrain.png")
        plt.close(fig)

        fig, ax = plt.subplots()
        ax.plot(x, y3)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax.set(xlabel='Time (s)', ylabel='IDrain (I)',
               title=filename[:-4] + "__IDrain\n")
        ax.grid()
        fig.savefig(temppath+filename[:-4]+"__IDrain.png")
        plt.close(fig)

        fig, ax = plt.subplots()
        ax.plot(y1, y3, 'r.')

        if any(yvalues < 0 for yvalues in y3):
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        else:
            ax.set_yscale("log")
        ax.set(xlabel='VBackGate (V)', ylabel='IDrain (I)',
               title=filename[:-4] + "__VBackgate_IDrain\n")
        ax.grid()
        fig.savefig(temppath + filename[:-4] + "__VBackgate_IDrain.png")
        plt.close(fig)


# plotting every file in relativepath
def filesystemplotfunction(relativepath):
    path = relativepath
    count = 0
    filepaths = []
    for filenamerec in glob.iglob(os.path.join(path, "**/*.crv"), recursive=True):
        # print(filenamerec)
        # fileplotfunction(filenamerec)         Single Process
        filepaths.append(filenamerec)
        count = count+1

    print("running...")
    print("Es wurden ", count, "Messdaten gefunden.")
    pool = Pool(os.cpu_count())  # Use all the CPUs available

    start_time = time.time()
    pool.map(fileplotfunction, filepaths)  # Multiprocess
    end_time = time.time()

    print("Es wurden", count*4, "Bilder geplottet, dies hat", end_time - start_time, "Sekunden gedauert")


def extractvaluesfromfile(pathtofile):
    if os.path.isfile(pathtofile):
        with open(pathtofile) as f:
            for i in range(6):                    # starting at line 11 where plot data starts
                f.__next__()
            data = f.read()

        data = data.split('\n')                   # splitting seperate lines
        data = [row.split('  ') for row in data]  # removing blanks
        data.pop()                                # remove last useless Array in crv

        vg = [float(column[2]) for column in data]  # VBackGate
        id = [float(column[4]) for column in data]  # IDrain

        # print("\nPath: "+pathtofile)

        # get Imax/Imin factor
        idfactor = max(id)/min(id)

        # get treshold at approx 10⁻⁶ or mean value since ids are so different dont now if solution is applicable
        meanid = sum(id)/len(id)

        #print("mean value of id: ", meanid)

        #getting end of first sweep
        endoffirstarray = vg.index(max(vg))
        # print("first sweep index at: ", vg.index(max(vg)))
        #splitting array in up and down sweep
        idn1 = np.asarray(id[:endoffirstarray+1])
        idn2 = np.asarray(id[endoffirstarray+1:])
        vg1 = vg[:endoffirstarray+1]
        vg2 = vg[endoffirstarray+1:]
        pos1 = (np.abs(idn1 - meanid)).argmin()
        pos2 = (np.abs(idn2 - meanid)).argmin()

        # print("FIRST ARRAY NEAREST: ", idn1[pos1])
        # print("SECOND ARRAY NEAREST: ", idn2[pos2])

        vth1 = vg1[pos1]
        vth2 = vg2[pos2]
        # print("VTH1: ", vth1)
        # print("VTH2: ", vth2)
        hyswidth = abs(vth1-vth2)

        returnlist = [vth1, idfactor, hyswidth]
        return returnlist


def comparedevices(directorypath, searchstrs):
    if not os.path.exists(directorypath):
        print("path does not exist")
        exit(-1)
    path = directorypath
    filepaths = []
    foundpaths = []
    for filenamerec in glob.iglob(os.path.join(path, "**/*.crv"), recursive=True):
        # print(filenamerec)
        filepaths.append(filenamerec)

    filepaths = sorted(filepaths)       # order list for pretty test printing purposes

    for singlepaths in filepaths:
        if all(singlesearchstr in singlepaths for singlesearchstr in searchstrs):  # checks for files with strings
            print(singlepaths)                                                    # from searchstr and prints them
            foundpaths.append(singlepaths)
    if not foundpaths:
        print("no filename which contains all keywords was found")
        exit(-1)

    newstring = foundpaths[0].split('/')
    #print(newstring)
    dirname1 = newstring[4]
    devicename = newstring[5]
    # filename = newstring[6]

    temppath = "../../Batchelor-Arbeit/Compare-Plots/"

    nameofnewfile = dirname1 + "_comparefile.crv"
    i = 0
    while os.path.isfile(temppath + nameofnewfile):
        i += 1
        nameofnewfile = dirname1 + "_comparefile%d.crv" % i

    file = open(temppath + nameofnewfile, "w")
    file.write("Devicename      threshold-voltage at mean value drain(V)        Id_max/Id_min(1)         Vth1-Vth2(V)\n")
    for devicepath in foundpaths:
        # get values from devicepath
        #print(devicepath)
        valuelist = extractvaluesfromfile(devicepath)
        # get description of device
        strpath = str(devicepath)
        pos1 = strpath.find("IdVg_")
        pos2 = strpath.find("_Vd")
        file.write("%s_%s %e %e %e\n" % (devicepath.split('/')[5],strpath[pos1+5:pos2],valuelist[0],valuelist[1],valuelist[2]))
    file.close()
