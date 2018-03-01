from multiprocessing import Pool
from textwrap import wrap
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
        with open(pathtofile) as f:
            for i in range(6):                    # starting at line 11 where plot data starts
                if i == 2:
                    timestring = f.readline()[13:33]
                f.__next__()
            data = f.read()
        #print(timestring)
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
        data = [row.split('  ') for row in data]  # removing blanks
        data.pop()                                # remove last useless Array in crv

        vg = [float(column[2]) for column in data]  # VBackGate
        idr = [abs(float(column[3])) for column in data]  # IDrain abs

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

        returnlist = [vth1, vth2, idmax, idmin]
        return returnlist


# comparing devices type2
def secondcomparedevices(directorypath, searchstrs, antisearch):
    if not os.path.exists(directorypath):
        print("path does not exist")
        exit(-1)
    path = directorypath
    filepaths = []
    foundpaths = []
    secondfoundpaths = []
    for filenamerec in glob.iglob(os.path.join(path, "**/*.txt"), recursive=True):
        # print(filenamerec)
        filepaths.append(filenamerec)

    filepaths = sorted(filepaths)       # order list for pretty test printing purposes
    for singlepaths in filepaths:
        if all(singlesearchstr in singlepaths for singlesearchstr in searchstrs):  # checks for files with strings
            # print(singlepaths)                                                    # from searchstr and prints them
            if not any(anti in singlepaths for anti in antisearch):
                foundpaths.append(singlepaths)
                #print(singlepaths)
    if not foundpaths:
        print("no filename which contains all keywords was found")
        return
    #print(foundpaths)

    nameofnewfile = "_".join(searchstrs) + "_Messdaten2_comparefile.crv"
    temppath = "../../Batchelor-Arbeit/Compare-Plots2/"

    foundpaths = sorted(foundpaths)
    file = open(temppath + directorypath.split('/')[4] + "_no[" + "_".join(antisearch) + "]" + nameofnewfile, "w")
    file.write("Devicename       Vth1(V)        Vth2(V)     Id_max(1)   Id_min(1)\n")
    for devicepath in foundpaths:
        # get values from devicepath
        # print(devicepath)
        valuelist = secondextractvaluesfromfile(devicepath)
        file.write("%s %e %e %e %e\n" % (devicepath.split('/')[6],
                                           valuelist[0], valuelist[1], valuelist[2], valuelist[3]))
        print(devicepath)
    file.close()
    with open(temppath + directorypath.split('/')[4] + "_no[" + "_".join(antisearch) + "]" + nameofnewfile) as f:

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

    fig.savefig(temppath + directorypath.split('/')[4] + "_" + nameofnewfile[:-4] + "_no[" + "_".join(antisearch) + "]_Imax_Imin.png", bbox_inches='tight', dpi=300)
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
    fig.tight_layout()
    fig.savefig(temppath + directorypath.split('/')[4] + "_" + nameofnewfile[:-4] + "_no[" + "_".join(antisearch) + "]_Vth1_Vth2.png", bbox_inches='tight',
                dpi=300)
    plt.close(fig)


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
        data = [row.split('  ') for row in data]  # removing blanks
        data.pop()  # remove last useless Array in crv
        # print(data)
        try:
            x = [float(column[0]) for column in data]        # time
        except Exception:
            with open(temppath+"error2.txt", "a") as f:
                f.write("Fehler in "+pathtofile+"\n")
            print("STRANGEFAIL")
            # secondfileplotfunction(pathtofile)
            return
        # y1 = [float(column[1]) for column in data]     # VDrain
        y2 = [float(column[2]) for column in data]       # VGate
        y3 = [abs(float(column[3])) for column in data]       # IDrain

        # print(newstring)

        # print(temppath)
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
        # useless code revisited since now all Id will be abs values
        #if any(yvalues < 0 for yvalues in y3):
        #    plt.ticklabel_format(style='sci', axis='y', scilimits=(0, 0))
        #else:
        ax.set_yscale("log")
        ax.set(xlabel='VBackGate (V)', ylabel='IDrain (I)')
        ax.grid()
        title = ax.set_title("\n".join(wrap((newstring[len(newstring) - 1])[:-4], 60)))
        fig.tight_layout()
        title.set_y(1.03)
        fig.savefig(temppath + (newstring[len(newstring)-1])[:-4] + "__VBackgate_IDrain.png")
        plt.close(fig)


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

