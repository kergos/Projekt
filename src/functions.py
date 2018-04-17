from multiprocessing import Pool
from textwrap import wrap
import matplotlib.pyplot as plt
import numpy as np
from scipy.constants import k, e
import os
import glob
import time
import random

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
        # y2 = [float(column[3]) for column in data]  #VDrain
        y3 = [abs(float(column[4])) for column in data]  #IDrain

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

        """
        fig, ax = plt.subplots()

        ax.plot(x, y1)
        ax.set(xlabel='Time (s)', ylabel='VBackGate (V)',
               title=filename[:-4] + "__VBackgate")
        ax.grid()
        fig.savefig(temppath+filename[:-4]+"__VBackgate.png")
        plt.close(fig)

        fig, ax = plt.subplots()
        ax.plot(x, y2)
        ax.set(xlabel='Time (s)', ylabel='VDrain (V)',
               title=filename[:-4] + "__VDrain\n")
        ax.grid()
        fig.savefig(temppath+filename[:-4]+"__VDrain.png")
        plt.close(fig)
        """
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

        """ useless code revisited since now all Id will be abs values
        if any(yvalues < 0 for yvalues in y3):
            plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        else:
        """
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

    print("Es wurden", count*2, "Bilder geplottet, dies hat", end_time - start_time, "Sekunden gedauert")


# extracting values from file
def extractvaluesfromfile(pathtofile):
    if os.path.isfile(pathtofile):
        timestring = ""
        with open(pathtofile) as f:
            for i in range(6):                    # starting at line 11 where plot data starts
                if i == 2:
                    timestring = f.readline()[13:33]
                f.__next__()
            data = f.read()
        # print(timestring)
        data = data.split('\n')                   # splitting seperate lines
        data = [row.split('  ') for row in data]  # removing blanks
        data.pop()                                # remove last useless Array in crv

        vg = [float(column[2]) for column in data]  # VBackGate
        idr = [abs(float(column[4])) for column in data]  # IDrain abs

        # print("\nPath: "+pathtofile)

        # get Imax/Imin
        tidr = np.array(idr)
        idmax = np.max(tidr[np.nonzero(tidr)])
        idmin = np.min(tidr[np.nonzero(tidr)])


        # get treshold at 10% of idr = vth1
        threshid = 0.1*idmax


        # getting end of first sweep
        endoffirstarray = vg.index(max(vg))
        # print("first sweep index at: ", vg.index(max(vg)))
        # splitting array in up and down sweep
        idn1 = np.asarray(idr[:endoffirstarray+1])
        idn2 = np.asarray(idr[endoffirstarray+1:])
        vg1 = vg[:endoffirstarray+1]
        vg2 = vg[endoffirstarray+1:]
        pos1 = (np.abs(idn1 - threshid)).argmin()
        pos2 = (np.abs(idn2 - threshid)).argmin()

        # print("FIRST ARRAY NEAREST: ", idn1[pos1])
        # print("SECOND ARRAY NEAREST: ", idn2[pos2])

        vth1 = vg1[pos1]
        vth2 = vg2[pos2]
        # print("VTH1: ", vth1)
        # print("VTH2: ", vth2)

        returnlist = [vth1, vth2, idmax, idmin, timestring]
        return returnlist


# comparing devices
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
        return

    newstring = foundpaths[0].split('/')
    #print(newstring)
    dirname1 = newstring[4]
    devicename = newstring[5]
    # filename = newstring[6]

    temppath = "../../Batchelor-Arbeit/Compare-Plots/"

    nameofnewfile = dirname1 + "_comparefile.crv"
    """
    i = 0
    while os.path.isfile(temppath + nameofnewfile):
        i += 1
        nameofnewfile = dirname1 + "_comparefile%d.crv" % i
    """
    filenameadd = "_".join(searchstrs) + "_"

    file = open(temppath + filenameadd + nameofnewfile, "w")
    file.write("Devicename     Vth1(V)        Vth2(V)     Id_max(1)   Id_min(1)     Timestamp\n")
    for devicepath in foundpaths:
        # get values from devicepath
        # print(devicepath)
        valuelist = extractvaluesfromfile(devicepath)
        # get description of device
        strpath = str(devicepath)
        pos1 = strpath.find("IdVg_")
        pos2 = strpath.find("_Vd")
        file.write("%s_%s %e %e %e %e %s\n" % (devicepath.split('/')[5], strpath[pos1 + 5:pos2],
                                                   valuelist[0], valuelist[1], valuelist[2], valuelist[3], valuelist[4]))
    file.close()

    with open(temppath + filenameadd + nameofnewfile) as f:
        f.__next__()  # starting at line 2 where plot data starts
        data = f.read()

    data = data.split('\n')                   # splitting seperate lines
    data = [row.split(' ') for row in data]  # removing blanks
    data.pop()

    # print(data)
    x = [column[0] for column in data]          # Devices
    y1 = [float(column[1]) for column in data]  # Vth1
    y2 = [float(column[2]) for column in data]  # Vth2
    y3 = [float(column[3]) for column in data]  # Idmax
    y4 = [float(column[4]) for column in data]  # Idmin

    barwidth = 0.3
    opacity = 1
    error_config = {'ecolor': '0.3'}

    # Imax/Imin Plot
    # CONDITION 1: Imax/Imin has to be bigger than 10³ for measuring to be counted as valid
    yifactor = [x / y for x, y in zip(y3, y4)]
    validfactors = []
    validdevices = []
    validvth1 = []
    validvth2 = []
    i = 0
    for factor in yifactor:
        if factor > 1e3:
            validfactors.append(factor)
            validdevices.append(x[i])
            validvth1.append(y1[i])
            validvth2.append(y2[i])
        i += 1
    fig, ax = plt.subplots()
    ax.set_yscale("log")
    index = np.arange(len(validdevices))
    ax.set_xticks(index)
    ax.set_xticklabels(validdevices)
    rects = ax.bar(index, validfactors, barwidth, alpha=opacity, color='orange',
                   error_kw=error_config)
    ax.set(xlabel='Devices', ylabel='Imax/Imin',
           title=nameofnewfile[:-4] + "\n")
    ax.grid()
    autolabel(rects, ax)

    fig.savefig(temppath + filenameadd + nameofnewfile[:-4] + "_Imax_Imin.png")
    plt.close(fig)

    # Vth1_Vth2 Plot
    fig, ax = plt.subplots()
    index = np.arange(len(validdevices))
    rect1 = ax.bar(index, validvth1, barwidth, alpha=opacity, color='b',
                   error_kw=error_config, label='Vth1')
    rect2 = ax.bar(index+barwidth, validvth2, barwidth,  alpha=opacity, color='g',
                   error_kw=error_config, label='Vth2')
    ax.set_xticks(index + barwidth / 2)
    ax.set_xticklabels(validdevices)
    ax.set(xlabel='Devices', ylabel='V_th',
           title=nameofnewfile[:-4] + "\n")
    autolabel(rect1, ax)
    autolabel(rect2, ax)
    ax.grid()
    ax.legend()
    fig.tight_layout()
    fig.savefig(temppath + filenameadd + nameofnewfile[:-4] + "_Vth1_Vth2.png")
    plt.close(fig)


# comparing recursively
def comparedevicesinfolder(multipledirpath, searchstrs):
    if not os.path.exists(multipledirpath):
        print("path does not exist")
        exit(-1)
    subpaths = os.listdir(multipledirpath)
    pathforfunction = []
    for path in subpaths:
        if path[0] is not ".":      # removes non existent "folders"
            pathforfunction.append(os.path.join(multipledirpath,path))
    # print(pathforfunction)
    for path in pathforfunction:
        comparedevices(path, searchstrs)


# extracting data type2
def secondextractvaluesfromfile(pathtofile):
    if os.path.isfile(pathtofile):
        with open(pathtofile) as f:
            f.__next__()
            data = f.read()
        data = data.split('\n')                   # splitting seperate lines
        datatemp = [row.split('  ') for row in data]  # removing blanks

        # checks if it is a different format (example if not seperated by "  " len(datatemp[0])
        # will be 1 so it needs to be seperated by tabs
        # only problem is that first data row gets axed but this is negligible
        if len(datatemp[0]) > 1:
            data = datatemp
        else:
            data = [row.split() for row in data]
        data.pop()  # remove last useless Array in crv
        vg = [float(column[2]) for column in data]  # VBackGate
        idr = [abs(float(column[3])) for column in data]  # IDrain abs

        # get Imax/Imin
        tvg = np.array(vg)
        tidr = np.array(idr)
        idmax = np.max(tidr[np.nonzero(tidr)])
        # minimum value wrong because of too high measuring resolution
        # idmin = np.min(tidr[np.nonzero(tidr)])
        # now it uses the last element in the crv which should be the lowest because of hysteresis
        idmin = idr[-1]

        # first we would get treshold at 10% of idr = vth1 but because of mos2-characteristics we now take only 1%
        threshid = 0.01*idmax

        # getting end of first sweep max finds the index of the first sweep maximum
        endoffirstarray = vg.index(max(vg))
        # print("first sweep index at: ", vg.index(max(vg)))
        # splitting array in up and down sweep
        idn1 = np.asarray(idr[:endoffirstarray+1])
        idn2 = np.asarray(idr[endoffirstarray+1:])
        vg1 = vg[:endoffirstarray+1]
        vg2 = vg[endoffirstarray+1:]
        # takes the abs between all values in the sweep and takes the smallest one and returns its index,
        # the smalles abs value stands for the smallest difference
        pos1 = (np.abs(idn1 - threshid)).argmin()
        pos2 = (np.abs(idn2 - threshid)).argmin()

        # print("FIRST ARRAY NEAREST: ", idn1[pos1])
        # print("SECOND ARRAY NEAREST: ", idn2[pos2])

        vth1 = vg1[pos1]
        vth2 = vg2[pos2]
        # print("VTH1: ", vth1)
        # print("VTH2: ", vth2)

        # getting Vmin which is the x value at Imin+50% originally 10% but that was too low too get a good fit
        idminplus = idmin * 1.5
        pos3 = (np.abs(idn2 - idminplus)).argmin()
        vmin = vg2[pos3]
        """
        print("IDminneu: ", idmin)
        print("Idmin+", idminplus)
        """

        # get index from vmin on backsweep if necessary
        minind = vg.index(vmin)
        # get index from vth2
        maxind = vg.index(vth2)
        # check if minind is on first sweep, if yes get minind on backsweep
        if abs(minind-maxind) > 100:
            # print("index difference too large -> changed min and max index for fit accordingly")
            # if difference is too big, after fix maxind is smaller than mindind
            # because it comes first on backsweep so in that case we need to swap minind and maxind
            minind = maxind
            maxind = len(vg1) + vg2.index(vmin)
        """
        print("vmin laut vg2(pos3):", vmin)
        print("index von vmin(minind):", minind)
        print("vth2:", vth2)
        print("index von vth2(maxind):", maxind)
        """

        # try to fit line from vmin to vth2
        fitvalue = np.polyfit(vg[minind:maxind], np.log(idr[minind:maxind]), 1)
        # slope for fit
        slope = 1/fitvalue[0] * np.log(10)

        # print("Steigung: ", slope)
        # print("fitvalue: ", fitvalue)

        # getting Temperature from path
        pathlist = pathtofile.split("/")
        T = pathlist[7][:-1]
        bakestat = "_notbkd"
        if "baked" in pathtofile:
            bakestat = "_bkd"
            T = pathlist[7][:-7]
        # C° + 273.15 = Kelvin
        T = (int(T) + 273.15)
        if T > 325.15:
            bakestat = ""
        slim = T * k / e * np.log(10)
        # Calculate Ct cox = epser/thickness
        cox = 3.9/90e-9
        # slope/slim = (ct+cox)/cox
        ct = ((slope/slim)*cox)-cox
        # Get Vd from path
        strindex = pathlist[9].find("Vd")
        dataset = (dict(T=T, Vg=tvg, Id=tidr, S2=slope, Slim=slim, Fit=fitvalue, Baked=bakestat, Device=pathlist[6],
                        Vd=pathlist[9][strindex:-4], Ct=ct))
        returnlist = [vth1, vth2, vmin, idmax, idmin, dataset]
        return returnlist


# comparing devices type2
def secondcomparedevices(directorypath, searchstrs, antisearch):
    if not os.path.exists(directorypath):
        print("path does not exist")
        exit(-1)
    path = directorypath
    filepaths = []
    foundpaths = []
    for filenamerec in glob.iglob(os.path.join(path, "**/*.txt"), recursive=True):
        # print(filenamerec)
        filepaths.append(filenamerec)

    filepaths = sorted(filepaths)       # order list for pretty test printing purposes
    for singlepaths in filepaths:
        if all(singlesearchstr in singlepaths for singlesearchstr in searchstrs):  # checks for files with strings
            # print(singlepaths)                                                    # from searchstr and prints them
            if not any(anti in singlepaths for anti in antisearch):
                foundpaths.append(singlepaths)
                # print(singlepaths)
    if not foundpaths:
        print("no filename which contains all keywords was found")
        return
    # print(foundpaths)

    nameofnewfile = "_".join(searchstrs) + "_Messdaten2_comparefile"
    temppath = "../../Batchelor-Arbeit/Compare-Plots2/"

    foundpaths = sorted(foundpaths)
    file = open(temppath + directorypath.split('/')[4] + "_" + nameofnewfile + "_no[" + "_".join(antisearch) + "].crv", "w")
    file.write("Devicename       Vth1(V)        Vth2(V)     Vmin(V)     Id_max(A)    Id_min(A)    Gradient[V/dec]    "
               "Capacity[F]\n")
    for devicepath in foundpaths:
        # get values from devicepath
        print(devicepath)
        valuelist = secondextractvaluesfromfile(devicepath)
        file.write("%s %e %e %e %e %e %e %e\n"
                   % (devicepath.split('/')[4]+"_"+devicepath.split('/')[5]+"_" + devicepath.split('/')[6],
                      valuelist[0], valuelist[1], valuelist[2], valuelist[3], valuelist[4], valuelist[5]['S2'], valuelist[5]['Ct']))
    file.close()

    with open(temppath + directorypath.split('/')[4] + "_" + nameofnewfile + "_no[" + "_".join(antisearch) + "].crv") as f:
        f.__next__()  # starting at line 2 where plot data starts
        data = f.read()

    data = data.split('\n')                   # splitting seperate lines
    data = [row.split(' ') for row in data]  # removing blanks
    data.pop()

    # print(data)
    # x = [column[0] for column in data]          # Devices
    x = ["\n".join(wrap(column[0], 5)) for column in data]          # Devices"\n".join(wrap((newstring[len(newstring) - 1])[:-4], 60))
    x.sort()
    y1 = [float(column[1]) for column in data]  # Vth1
    y2 = [float(column[2]) for column in data]  # Vth2
    y3 = [float(column[4]) for column in data]  # Idmax
    y4 = [float(column[5]) for column in data]  # Idmin
    y6 = [float(column[6]) for column in data]  # Gradient

    barwidth = 0.3
    opacity = 1
    error_config = {'ecolor': '0.3'}

    # Imax/Imin Plot
    # CONDITION 1: Imax/Imin has to be bigger than 10³ for measuring to be counted as valid
    yifactor = [x / y for x, y in zip(y3, y4)]
    validfactors = []
    validdevices = []
    validvth1 = []
    validvth2 = []
    validgrad = []
    i = 0
    for factor in yifactor:
        if factor > 1e3:
            validfactors.append(factor)
            validdevices.append(x[i])
            validvth1.append(y1[i])
            validvth2.append(y2[i])
            validgrad.append(y6[i])
        i += 1
    # time measuring start
    start_time = time.time()
    fig, ax = plt.subplots()
    ax.set_yscale("log")
    fig.set_size_inches(len(x), 10)
    index = np.arange(len(validdevices))
    ax.set_xticks(index)
    ax.set_xticklabels(validdevices)
    rects = ax.bar(index, validfactors, barwidth, alpha=opacity, color='orange',
                   error_kw=error_config)
    ax.set(xlabel='Devices', ylabel='Imax/Imin',
           title=nameofnewfile[:-4] + "_no[" + "_".join(antisearch) + "]" + "\n")
    ax.grid()
    autolabel(rects, ax)

    fig.savefig(temppath + directorypath.split('/')[4] + "_" + nameofnewfile[:-4] + "_no["
                + "_".join(antisearch) + "]_Imax_Imin.png", bbox_inches='tight', dpi=300)
    plt.close(fig)

    # Hystogramm over the Ifactors
    fig, ax = plt.subplots()
    ax.grid()
    # Get Probability Density Function
    mean = np.mean(validfactors)
    var = np.var(validfactors)
    pdf = []
    validfactors = sorted(validfactors)
    for xi in validfactors:
        pdf.append(1/(np.sqrt(2*np.pi*var))*np.exp(-np.power((xi-mean), 2)/(2*var)))
    ax.plot(validfactors, pdf, '-.')
    # now histogramm
    plt.hist(validfactors, bins='auto', density=True, facecolor='orange', alpha=0.75)
    ax.set(xlabel='Idmax/Idmin', ylabel='Probability',
           title=nameofnewfile[:-4] + "_no[" + "_".join(antisearch) + "]" + "\n")
    ax.set_xscale("log")
    fig.savefig(temppath + directorypath.split('/')[4] + "_" + nameofnewfile[:-4] + "_no["
                + "_".join(antisearch) + "]_Imax_Imin_Histogram.png", bbox_inches='tight', dpi=300)
    plt.close(fig)

    # Vth1_Vth2 Plot
    fig, ax = plt.subplots()
    fig.set_size_inches(len(x), 10)
    index = np.arange(len(validdevices))
    rect1 = ax.bar(index, validvth1, barwidth, alpha=opacity, color='b',
                   error_kw=error_config, label='Vth1')
    rect2 = ax.bar(index+barwidth, validvth2, barwidth,  alpha=opacity, color='g',
                   error_kw=error_config, label='Vth2')
    ax.set_xticks(index + barwidth / 2)
    ax.set_xticklabels(validdevices)
    ax.set(xlabel='Devices', ylabel='V_th',
           title=nameofnewfile[:-4] + "_no[" + "_".join(antisearch) + "]" + "\n")
    autolabel(rect1, ax)
    autolabel(rect2, ax)
    ax.grid()
    ax.legend()
    # avoiding strange left cannot >= right error from matplotlib
    if len(index) > 5:
        fig.tight_layout()
    fig.savefig(temppath + directorypath.split('/')[4] + "_" + nameofnewfile[:-4] + "_no["
                + "_".join(antisearch) + "]_Vth1_Vth2.png", bbox_inches='tight',
                dpi=300)
    plt.close(fig)

    # Hystogramm over Vth2
    fig, ax = plt.subplots()
    ax.grid()
    # Get Probability Density Function
    mean = np.mean(validvth2)
    var = np.var(validvth2)
    pdf = []
    validvth2 = sorted(validvth2)
    for xi in validvth2:
        pdf.append(1 / (np.sqrt(2 * np.pi * var)) * np.exp(-np.power((xi - mean), 2) / (2 * var)))
    ax.plot(validvth2, pdf, '-.')
    # now histogramm
    plt.hist(validvth2, bins='auto', density=True, facecolor='g', alpha=0.75)
    ax.set(xlabel='Vth2', ylabel='Probability',
           title=nameofnewfile[:-4] + "_no[" + "_".join(antisearch) + "]" + "\n")
    fig.savefig(temppath + directorypath.split('/')[4] + "_" + nameofnewfile[:-4] + "_no["
                + "_".join(antisearch) + "]_Vth2_Histogram.png", bbox_inches='tight', dpi=300)
    plt.close(fig)

    # Hystogramm over Vthdelta
    fig, ax = plt.subplots()
    ax.grid()
    # Get Probability Density Function
    vthdelta = [abs(a-b) for a, b in zip(validvth1, validvth2)]
    mean = np.mean(vthdelta)
    var = np.var(vthdelta)
    pdf = []
    vthdelta = sorted(vthdelta)
    for xi in vthdelta:
        pdf.append(1 / (np.sqrt(2 * np.pi * var)) * np.exp(-np.power((xi - mean), 2) / (2 * var)))
    ax.plot(vthdelta, pdf, '-.')
    # now histogramm
    plt.hist(vthdelta, bins='auto', density=True, facecolor='g', alpha=0.75)
    ax.set(xlabel='Vthdelta', ylabel='Probability',
           title=nameofnewfile[:-4] + "_no[" + "_".join(antisearch) + "]" + "\n")
    fig.savefig(temppath + directorypath.split('/')[4] + "_" + nameofnewfile[:-4] + "_no["
                + "_".join(antisearch) + "]_Vthdelta_Histogram.png", bbox_inches='tight', dpi=300)
    plt.close(fig)

    # Hystogramm over Gradient
    fig, ax = plt.subplots()
    ax.grid()
    # Get Probability Density Function
    mean = np.mean(validgrad)
    var = np.var(validgrad)
    pdf = []
    validgrad = sorted(validgrad)
    for xi in validgrad:
        pdf.append(1 / (np.sqrt(2 * np.pi * var)) * np.exp(-np.power((xi - mean), 2) / (2 * var)))
    ax.plot(validgrad, pdf, '-.')
    # now histogramm
    plt.hist(validgrad, bins='auto', density=True, facecolor='g', alpha=0.75)
    ax.set(xlabel='Gradient [V/dec]', ylabel='Probability',
           title=nameofnewfile[:-4] + "_no[" + "_".join(antisearch) + "]" + "\n")
    fig.savefig(temppath + directorypath.split('/')[4] + "_" + nameofnewfile[:-4] + "_no["
                + "_".join(antisearch) + "]_Gradient_Histogram.png", bbox_inches='tight', dpi=300)
    plt.close(fig)


    # time measuring end
    end_time = time.time()
    print("Plot hat", end_time - start_time, "Sekunden gedauert")


# plotting fits
def plotfit(datasets, searchstrs):
    plt.figure()
    path = "../../Batchelor-Arbeit/Fit-Plots2/"
    t = []
    s2 = []
    slim = []

    for j, dataset in enumerate(datasets):
        t.append(dataset['T'])
        s2.append(dataset['S2'])
        slim.append(dataset['Slim'])

        # get random color
        rcolor = ('#%02X%02X%02X' % (randint(), randint(), randint()))
        plt.ylabel(r'log$(I_\mathrm{D})$ [A]')
        plt.xlabel(r'$V_\mathrm{G} \: [\mathrm{V}]$')
        plt.ylim(-11, -1)
        plt.plot(dataset['Vg'], np.log(np.abs(dataset['Id'][0:len(dataset['Id'])])) / np.log(10), marker='.',
                 markersize=5, color=rcolor, linestyle=' ', label=dataset['Device'] + "_" + dataset['Vd'] + "_" + str(dataset['T']) + "K" + dataset['Baked'])
        plt.plot(dataset['Vg'], (dataset['Vg'] * dataset["Fit"][0] + dataset["Fit"][1]) / np.log(10), color=rcolor)
        plt.text(-4, -13-j, "S = " + "{:.3f}".format(dataset['S2']) + "V/dec.", color=rcolor)

    plt.legend(loc=2, bbox_to_anchor=(1.05, 1.15), prop={'size': 14}, borderpad=0.4, labelspacing=0.1)
    plt.xlim(-15, 20)
    plt.ylim(-11, -1)
    plt.savefig(path + searchstrs + "_IdVg_all.pdf", bbox_inches='tight')

    plt.close()

    plt.figure()
    plt.ylabel(r'S [V/dec.]')
    plt.xlabel(r'T [K]')
    plt.plot(t, s2, color="#990000", marker='x', markersize=10, markeredgewidth=2)
    plt.plot(t, slim, color="#000099", marker='x', markersize=10, markeredgewidth=2)
    ax = plt.gca()
    ax.set_yscale('log')
    plt.savefig(path + searchstrs + "_S_T_log.pdf", bbox_inches='tight')

    plt.close()

    plt.figure()
    plt.ylabel(r'S [V/dec.]')
    plt.xlabel(r'T [K]')
    plt.plot(t, s2, color="#990000", marker='x', markersize=10, markeredgewidth=2)
    plt.plot(t, slim, color="#000099", marker='x', markersize=10, markeredgewidth=2)
    ax = plt.gca()
    # ax.text(100, 1, " Cont.")
    plt.savefig(path + searchstrs + "_S_T_ar.pdf", bbox_inches='tight')

    plt.close()


# fitting devices type2
def secondfit(directorypath, searchstrs, antisearch):
    if not os.path.exists(directorypath):
        print("path does not exist")
        exit(-1)
    path = directorypath
    filepaths = []
    foundpaths = []
    for filenamerec in glob.iglob(os.path.join(path, "**/*.txt"), recursive=True):
        filepaths.append(filenamerec)
    filepaths = sorted(filepaths)
    for singlepaths in filepaths:
        if all(singlesearchstr in singlepaths for singlesearchstr in searchstrs):       # any instead of all
            if not any(anti in singlepaths for anti in antisearch):
                foundpaths.append(singlepaths)
    if not foundpaths:
        print("no filename which contains all keywords was found")
        return
    foundpaths = sorted(foundpaths)
    datasets = []
    device = foundpaths[0].split("/")[6]
    for devicepath in foundpaths:
        print(devicepath)
        if devicepath.split("/")[6] == device:
            valuelist = secondextractvaluesfromfile(devicepath)
            datasets.append(valuelist[5])
        else:
            plotfit(datasets, device)
            datasets.clear()
            device = devicepath.split("/")[6]
            valuelist = secondextractvaluesfromfile(devicepath)
            datasets.append(valuelist[5])
    plotfit(datasets, device)

# multiple plots from one .crv file and creating type2
def secondfileplotfunction(pathtofile):
    if os.path.isfile(pathtofile):
        #print(pathtofile)
        temppath = "../../Batchelor-Arbeit/Plots2/"
        newstring = pathtofile.split('/')
        newstring = newstring[4:]
        with open(pathtofile) as f:                   # starting at line 2 where plot data starts
            f.__next__()
            data = f.read()
        data = data.split('\n')  # splitting seperate lines
        datatemp = [row.split('  ') for row in data]  # removing blanks

        # checks if it is a different format (example if not seperated by "  " len(datatemp[0])
        # will be 1 so it needs to be seperated by tabs
        # only problem is that first data row gets axed but this is negligible
        if len(datatemp[0]) > 1:
            data = datatemp
        else:
            data = [row.split() for row in data]
        data.pop()  # remove last useless Array in crv
        #print(data)
        try:
            x = [float(column[0]) for column in data]        # time
        except Exception:
            with open(temppath+"error2.txt", "a") as f:
                f.write("Fehler in "+pathtofile+"\n")
            print("failed to plot: "+pathtofile)
            return
        # y1 = [float(column[1]) for column in data]     # VDrain
        y2 = [float(column[2]) for column in data]       # VGate
        y3 = [abs(float(column[3])) for column in data]       # IDrain

        for pathpiece in newstring[:-1]:
            # print(pathpiece)
            temppath = os.path.join(temppath, pathpiece+"/")
            if not os.path.exists(temppath):
                os.makedirs(temppath)
            # print(temppath)
        # print(newstring[len(newstring)-1])

        fig, ax = plt.subplots()
        ax.plot(x, y3)
        plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        ax.set(xlabel='Time (s)', ylabel='IDrain (I)')
        ax.grid()
        title = ax.set_title("\n".join(wrap((newstring[len(newstring) - 1])[:-4], 60)))
        fig.tight_layout()
        title.set_y(1.03)
        fig.savefig(temppath + (newstring[len(newstring)-1])[:-4] + "__IDrain.png")
        plt.close(fig)

        fig, ax = plt.subplots()
        ax.plot(y2, y3, 'r.')
        # useless code since now all Id will be abs values
        #if any(yvalues < 0 for yvalues in y3):
        #    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        #else:
        # if wanted, you can set other x ticks here
        #ax.xaxis.set_major_locator(ticker.MultipleLocator(2.5))
        ax.set_yscale("log")
        ax.set(xlabel='VBackGate (V)', ylabel='IDrain (I)')
        ax.grid()
        title = ax.set_title("\n".join(wrap((newstring[len(newstring) - 1])[:-4], 60)))
        fig.tight_layout()
        title.set_y(1.03)
        fig.savefig(temppath + (newstring[len(newstring)-1])[:-4] + "__VBackgate_IDrain.png")
        plt.close(fig)
    else:
        print("File not found")


# plotting every file in relativepath type2
def secondfilesystemplotfunction(relativepath):
    path = relativepath
    filepaths = []
    validfilepaths = []
    count = 0
    for filenamerec in glob.iglob(os.path.join(path, "**/*.txt"), recursive=True):
        #print(filenamerec)
        filepaths.append(filenamerec)
    # filtering logfiles for they are useless
    for singlepath in filepaths:
        if "logfile" not in singlepath:
            print(singlepath)
            validfilepaths.append(singlepath)
            count += 1
    #print(validfilepaths)
    print("running...")
    print("Es wurden ", count, "Messdaten gefunden.")
    pool = Pool(os.cpu_count())  # Use all the CPUs available

    start_time = time.time()
    pool.map(secondfileplotfunction, validfilepaths)  # Multiprocess
    end_time = time.time()

    print("Es wurden", count * 2, "Bilder geplottet, dies hat", end_time - start_time, "Sekunden gedauert")


def autolabel(rects, ax):
    """
    Attach a text label above each bar displaying its height
    """
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2., 1.05*height,
                '%g' % height,
                ha='center', va='bottom')


def randint():
    return random.randint(0, 255)
