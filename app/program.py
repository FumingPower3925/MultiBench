# graphic design
import os
from time import sleep
import tkinter as tk
from tkinter import ttk, Canvas
from ttkthemes import ThemedTk
# show stats
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import json
import common
import distro
import subprocess
from common import *

# get distribution name and version
distribution = distro.name() + ' ' + distro.version()

# check if the required csv files exists, else creates them with the default values
for i in filenames:
    if not os.path.isfile(filepath+i) or not os.path.exists(filepath+i):
        os.system("touch " + filepath+i)
        if i == filenames[0]:
            os.system("echo 'distribution,execution time,events per second' >> " + filepath+i)
        elif i == filenames[1]:
            os.system("echo 'distribution,type of operations,throughput' >> " + filepath+i)
        elif i == filenames[2]:
            os.system("echo 'distribution,number of threads,number of operations per second,MiB per second' >> " + filepath+i)
        elif i == filenames[3]:
            os.system("echo 'distribution,number of threads,totalTime,latency average (ms)' >> " + filepath+i)

# create the widgets in the menu
def showMenuWindow(window):
    if window: window.destroy()

    #main window
    menuWindow = ThemedTk(theme=this_theme)
    menuWindow.title(menuString)
    menuWindow.geometry(menuResolution)

    # do a benchmark button
    common.createButton(menuWindow, doBenchmarkString, lambda: showBenchmarkWindow(menuWindow)).place(x=150,y=100)
    # show stats button
    common.createButton(menuWindow, viewStatsString, lambda: showStatsWindow(menuWindow)).place(x=500,y=100)
    # exit button
    common.createButton(menuWindow, exitString, lambda: common.quit_program(menuWindow)).place(x=665,y=350)

    menuWindow.mainloop()

# show the benchmarks page to customize it
def showBenchmarkWindow(menuWindow):
    menuWindow.destroy()
    #window to do the benchmarks
    benchmarkWindow = ThemedTk(theme=this_theme)
    benchmarkWindow.title(yourBenchmarksString)
    benchmarkWindow.geometry(defaultResolution)

    #create basic buttons
    createBasicButtons(benchmarkWindow)
    common.createButton(benchmarkWindow, benchString[0], showSysbenchOptions).place(x=posTestsButton[0],y=posTestsButton[1])

def showSysbenchOptions():
    sysbenchOptionsWindow = ThemedTk(theme=this_theme)
    sysbenchOptionsWindow.title(customizeBenchmarkString)
    sysbenchOptionsWindow.geometry(smallResolution)
    result = [tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()]
    tk.Checkbutton(sysbenchOptionsWindow, text=testString[0], command=lambda: result[0].set(not result[0].get())).pack()
    tk.Checkbutton(sysbenchOptionsWindow, text=testString[1], command=lambda: result[1].set(not result[1].get())).pack()
    tk.Checkbutton(sysbenchOptionsWindow, text=testString[2], command=lambda: result[2].set(not result[2].get())).pack()
    tk.Checkbutton(sysbenchOptionsWindow, text=testString[3], command=lambda: result[3].set(not result[3].get())).pack()
    common.createButton(sysbenchOptionsWindow, runString, lambda: runSysbench(sysbenchOptionsWindow, result)).pack()
    common.createButton(sysbenchOptionsWindow, returnString, lambda: sysbenchOptionsWindow.destroy()).pack()
    
def writeToWindow(window, text):
    tk.Label(window, text=text).pack()

def runSysbench(optionsWindow, result):
    optionsWindow.destroy()
    #window to show the progress
    sysbenchRunWindow = ThemedTk(theme=this_theme)
    sysbenchRunWindow.title(benchmarksRunningString)
    sysbenchRunWindow.geometry(smallResolution)
    # CPU Test
    if result[0].get():
        writeToWindow(sysbenchRunWindow, runningString[0])
        process = subprocess.Popen(['sysbench', 'cpu', '--cpu-max-prime=20000', '--threads=2', 'run'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        while (process.poll() is None):
            sleep(0.1)
        
        # Filtering the output
        std = stdout.decode()
        start = std.find("events per second:")
        end = std.find("\n", start)
        events = std[start+18:end].split()[0]
        start = std.find("total time:")
        end = std.find("\n", start)
        time = std[start+13:end-1].split()[0]

        # Writting the results to the CSV
        toWrite = distribution + ',' + time + ',' + events
        os.system("echo " + toWrite + " >> " + filepath+filenames[0])

    # FileIO Test
    if result[1].get():
        # File prepare
        tk.Label(sysbenchRunWindow, text=runningString[1]).pack()
        process = subprocess.Popen(['sysbench', 'fileio', '--file-total-size=32G', 'prepare'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        while (process.poll() is None):
            sleep(0.1)

        # File run
        tk.Label(sysbenchRunWindow, text=runningString[2]).pack()
        process = subprocess.Popen(['sysbench', 'fileio', '--file-total-size=32G', '--file-test-mode=rndrw', '--time=300', '--max-requests=0', 'run'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        while (process.poll() is None):
            sleep(0.1)

        # Filtering the output
        std = stdout.decode()
        start = std.find("read, MiB/s:")
        end = std.find("\n", start)
        readThroughput = std[start+12:end].split()[0]
        start = std.find("written, MiB/s:")
        end = std.find("\n", start)
        writeThroughput = std[start+15:end].split()[0]

        # Writting the results to the CSV
        toWrite = distribution + ',read throughput,' + readThroughput
        os.system("echo " + toWrite + " >> " + filepath+filenames[1])
        toWrite = distribution + ',write throughput,' + writeThroughput
        os.system("echo " + toWrite + " >> " + filepath+filenames[1])

        # File cleanup
        tk.Label(sysbenchRunWindow, text=runningString[3]).pack()
        process = subprocess.Popen(['sysbench', 'fileio', '--file-total-size=32G', '--file-test-mode=rndrw', '--time=300', '--max-requests=0', 'cleanup'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        while (process.poll() is None):
            sleep(0.1)

    # Memory
    if result[2].get():
        tk.Label(sysbenchRunWindow, text=runningString[4]).pack()
        process = subprocess.Popen(['sysbench', 'memory', '--threads=4', 'run'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        while (process.poll() is None):
            sleep(0.1)

        # Filtering the output
        
        std = stdout.decode()
        start = std.find("Total operations:")
        start = std.find("(", start)
        end = std.find("\n", start)
        numberOperations = std[start+1:end].split()[0]
        start = std.find("Number of threads:")
        end = std.find("\n", start)
        threads = std[start+18:end].split()[0]
        start = std.find("MiB transferred (")
        end = std.find("\n", start)
        mbPerSecond = std[start+17:end].split()[0]

        # Writting the results to the CSV
        toWrite = distribution + ',' + threads + ' threads,' + numberOperations + ',' + mbPerSecond
        os.system("echo " + toWrite + " >> " + filepath+filenames[2])
        

    # Threads
    if result[3].get():
        tk.Label(sysbenchRunWindow, text=runningString[5]).pack()
        process = subprocess.Popen(['sysbench', 'threads', '--thread-locks=1', '--time=20', 'run'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        while (process.poll() is None):
            sleep(0.1)

        # Filtering the output
        
        std = stdout.decode()
        start = std.find("total time:")
        end = std.find("\n", start)
        time = std[start+11:end-1].split()[0]
        start = std.find("Number of threads:")
        end = std.find("\n", start)
        threads = std[start+18:end].split()[0]
        start = std.find("avg:")
        end = std.find("\n", start)
        latency = std[start+18:end].split()[0]

        # Writting the results to the CSV
        toWrite = distribution + ',' + threads + ' threads,' + time + ',' + latency
        os.system("echo " + toWrite + " >> " + filepath+filenames[3])
        
    tk.Label(sysbenchRunWindow, text=finishString).pack()
    sleep(1)
    sysbenchRunWindow.destroy()

# show the stats of the benchmarks you have done
def showStatsWindow(menuWindow):
    # initialize basic widgets of the window
    menuWindow.destroy()
    statsWindow = ThemedTk(theme=this_theme)
    statsWindow.title(yourBenchmarksString)
    statsWindow.geometry(defaultResolution)

    #create basic buttons
    createBasicButtons(statsWindow)
    createShowTestButtons(statsWindow)

    # configure the 4 plots to have the same style
    sns.set_style('darkgrid')

def createBasicButtons(window):
    # button to return to the menu
    common.createButton(window, menuString, lambda: showMenuWindow(window)).place(x=posMenuButton[0],y=posMenuButton[1])
    # button to exit the app
    common.createButton(window, exitString, lambda: common.quit_program(window)).place(x=posExitButton[0],y=posExitButton[1])

def createShowTestButtons(window):
    common.createButton(window, testString[0], showCpuTestWindow).place(x=posTestsButton[0],y=posTestsButton[1])
    common.createButton(window, testString[1], showFileioTestWindow).place(x=posTestsButton[2],y=posTestsButton[3])
    common.createButton(window, testString[2], showMemoryTestWindow).place(x=posTestsButton[4],y=posTestsButton[5])
    common.createButton(window, testString[3], showThreadsTestWindow).place(x=posTestsButton[6],y=posTestsButton[7])

def showCpuTestWindow():
    cpuTestData = pd.read_csv(filepath+filenames[0])
    sns.barplot(x=cpuTestData["distribution"], y=cpuTestData["events per second"], data=cpuTestData, palette=barplotPalette)
    plt.title(testString[0])
    plt.show()

def showFileioTestWindow():
    fileioTestData = pd.read_csv(filepath+filenames[1])
    sns.barplot(x=fileioTestData["distribution"], y=fileioTestData["throughput"], hue=fileioTestData["type of operations"], data=fileioTestData, palette=barplotPalette)
    plt.title(testString[1])
    plt.show()

def showMemoryTestWindow():
    memoryTestData = pd.read_csv(filepath+filenames[2])
    sns.barplot(x=memoryTestData["distribution"], y=memoryTestData["number of operations per second"], hue=memoryTestData["number of threads"], palette=barplotPalette)
    plt.title(testString[2])
    plt.show()

    sns.barplot(x=memoryTestData["distribution"], y=memoryTestData["MiB per second"], hue=memoryTestData["number of threads"], palette=barplotPalette)
    plt.title(testString[2])
    plt.show()

def showThreadsTestWindow():
    threadsTestData = pd.read_csv(filepath+filenames[3])
    sns.barplot(x=threadsTestData["distribution"], y=threadsTestData["latency average (ms)"], hue=threadsTestData["number of threads"], palette=barplotPalette)
    plt.title(testString[3])
    plt.show()

# main
showMenuWindow(None)