import matplotlib.pyplot as plt
import numpy as np
import os
import glob
import time


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


def fileplotfunction(pathtofile):
    if os.path.isfile(pathtofile):
        with open(pathtofile) as f:
            for i in range(6):                    # starting at line 11 where plot data starts
                f.__next__()
            data = f.read()

        data = data.split('\n')                   # splitting seperate lines
        data = [row.split('  ') for row in data]  # removing blanks
        data.pop()                                # remove last useless Array in crv

        x = [float(column[1]) for column in data]
        y1 = [float(column[2]) for column in data]
        y2 = [float(column[3]) for column in data]
        y3 = [float(column[4]) for column in data]

        # string manipulation for naming purposes
        newstring = pathtofile.split('/')
        # print(newstring)
        dirname1 = newstring[4]
        dirname2 = newstring[5]
        filename = newstring[6]

        #print(pathtofile)
        #print(dirname1, dirname2, filename[:-4])

        temppath = "../../Batchelor-Arbeit/Plots/"
        
        if not os.path.exists(os.path.join(temppath, dirname1)):
            os.makedirs(os.path.join(temppath, dirname1))

        temppath = os.path.join(temppath, dirname1)

        if not os.path.exists(os.path.join(temppath, dirname2)):
            os.makedirs(os.path.join(temppath, dirname2))

        temppath = os.path.join(temppath, dirname2)+"/"
        #print(temppath)

        fig, ax = plt.subplots()
        ax.plot(x, y1)
        ax.set(xlabel='Time (s)', ylabel='VBackGate (V)',
               title=filename[:-4] + "__VBackgate")
        ax.grid()
        fig.savefig(temppath+filename[:-4]+"__VBackgate.png")

        #fig, ax = plt.subplots()
        plt.clf

        ax.plot(x, y2)
        ax.set(xlabel='Time (s)', ylabel='VDrain (V)',
               title=filename[:-4] + "__VDrain")
        ax.grid()
        fig.savefig(temppath+filename[:-4]+"__VDrain.png")

        #fig, ax = plt.subplots()
        plt.clf()

        ax.plot(x, y3)
        ax.set(xlabel='Time (s)', ylabel='IDrain (I)',
               title=filename[:-4] + "__IDrain")
        ax.grid()
        fig.savefig(temppath+filename[:-4]+"__IDrain.png")

        plt.clf() #clears figure
        plt.close(fig) #closes window


def filesystemplotfunction(relativepath):
    path = relativepath
    count = 0
    start_time = time.time()

    for filenamerec in glob.iglob(os.path.join(path, "**/*.crv"), recursive=True):
        # print(filenamerec)
        fileplotfunction(filenamerec)
        count = count+1

    end_time = time.time()
    print("Es wurden", count*3, "Bilder geplottet, dies hat", end_time - start_time, "Sekunden gedauert")
