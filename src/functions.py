import matplotlib.pyplot as plt
import numpy as np
import os
import glob
from pathlib import Path


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
            for i in range(6):      # starting at line 11 where plot data starts
                f.__next__()
            data = f.read()

        data = data.split('\n') #splitting seperate lines
        #print(data)
        data = [row.split('  ') for row in data] #removing blanks
        data.pop() #remove last useless Array
        x  = [float(column[1]) for column in data]
        y1 = [float(column[2]) for column in data]
        y2 = [float(column[3]) for column in data]
        y3 = [float(column[4]) for column in data]

        #string manipulation for naming purposes
        newstring = pathtofile.split('/')
        print(newstring)
        dirname1 = newstring[4]
        dirname2 = newstring[5]
        filename = newstring[6]
        print( dirname1, dirname2 , filename[:-4])
        """

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
        """

def filesystemplotfunction():
    path = '../../Batchelor-Arbeit/Messdaten/'  #put relative path to  here

    """

    for filename in os.listdir(path):       #looks for things in path
        #print(filename)
        if os.path.isdir(os.path.join(path,filename)):  #if thing in path is a dir print it
            print(filename,"")
            for filename2 in os.listdir(os.path.join(path,filename)):
                #print(filename2)
                if os.path.isdir(os.path.join(path, filename,filename2)):   #if thing in path is dir print it
                    print("-",filename2)
                    for filename3 in glob.glob(os.path.join(path,filename,filename2,"*.crv")):
                        print("--",filename3)
    """
    for filenamerec in glob.iglob(os.path.join(path,"**/*.crv"),recursive=True):
        #print(filenamerec)
        fileplotfunction(filenamerec)