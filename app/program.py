# graphic design
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
import subprocess

# initialize common constant variables
menuRes = common.menuResolution
defaultRes = common.defaultResolution
menuStr = common.menuString
doBenchmarkStr = common.doBenchmarkString
viewStatsStr = common.viewStatsString
customizeBenchmarkStr = common.customizeBenchmarkString
exitStr = common.exitString
theme = common.this_theme
yourBenchmarksStr = common.yourBenchmarksString
posMenuButton = common.posMenuButton
posExitButton = common.posExitButton
testStr = common.testString
benchStr = common.benchString
runStr = common.runString
runningStr = common.runningString
posTestsButton = common.posTestsButton
barplotPalette = common.barplotPalette
filepath = common.filepath
filenames = common.filenames

# create the widgets in the menu
def showMenuWindow(window):
    if window: window.destroy()

    #main window
    menuWindow = ThemedTk(theme=theme)
    menuWindow.title(menuStr)
    menuWindow.geometry(menuRes)

    # do a benchmark button
    common.createButton(menuWindow, doBenchmarkStr, lambda: showBenchmarkWindow(menuWindow)).place(x=150,y=100)
    # show stats button
    common.createButton(menuWindow, viewStatsStr, lambda: showStatsWindow(menuWindow)).place(x=500,y=100)
    # exit button
    common.createButton(menuWindow, exitStr, lambda: common.quit_program(menuWindow)).place(x=665,y=350)

    menuWindow.mainloop()

# show the benchmarks page to customize it
def showBenchmarkWindow(menuWindow):
    menuWindow.destroy()
    #window to do the benchmarks
    benchmarkWindow = ThemedTk(theme=theme)
    benchmarkWindow.title(yourBenchmarksStr)
    benchmarkWindow.geometry(defaultRes)

    #create basic buttons
    createBasicButtons(benchmarkWindow)
    common.createButton(benchmarkWindow, benchStr[0], showSysbenchOptions).place(x=posTestsButton[0],y=posTestsButton[1])

def showSysbenchOptions():
    sysbenchOptionsWindow = ThemedTk(theme=theme)
    sysbenchOptionsWindow.title(customizeBenchmarkStr)
    sysbenchOptionsWindow.geometry(menuRes)
    result = [tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar(), tk.BooleanVar()]
    tk.Checkbutton(sysbenchOptionsWindow, text=testStr[0], command=lambda: result[0].set(not result[0].get())).pack()
    tk.Checkbutton(sysbenchOptionsWindow, text=testStr[1], command=lambda: result[1].set(not result[1].get())).pack()
    tk.Checkbutton(sysbenchOptionsWindow, text=testStr[2], command=lambda: result[2].set(not result[2].get())).pack()
    tk.Checkbutton(sysbenchOptionsWindow, text=testStr[3], command=lambda: result[3].set(not result[3].get())).pack()
    common.createButton(sysbenchOptionsWindow, runStr, lambda: runSysbench(sysbenchOptionsWindow, result)).pack()

def runSysbench(window, result):
    # CPU Test
    if result[0].get():
        print(runningStr[0])
        process = subprocess.Popen(['sysbench', 'cpu', '--cpu-max-prime=20000', '--threads=2', 'run'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        while (process.poll() is None):
            sleep(0.1)
        print(stdout)
        print(stderr)

    # FileIO Test
    if result[1].get():
        # File prepare
        print(runningStr[1])
        process = subprocess.Popen(['sysbench', 'fileio', '--file-total-size=32G', 'prepare'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        while (process.poll() is None):
            sleep(0.1)

        # File run
        print(runningStr[2])
        process = subprocess.Popen(['sysbench', 'fileio', '--file-total-size=32G', '--file-test-mode=rndrw', '--max-time=300', '--max-requests=0', 'run'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        while (process.poll() is None):
            sleep(0.1)
        print(stdout)
        print(stderr)

        # File cleanup
        print(runningStr[3])
        process = subprocess.Popen(['sysbench', 'fileio', '--file-total-size=32G', '--file-test-mode=rndrw', '--max-time=300', '--max-requests=0', 'cleanup'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        while (process.poll() is None):
            sleep(0.1)

    # Memory
    if result[2].get():
        print(runningStr[4])
        process = subprocess.Popen(['sysbench', 'memory', '--threads=4', 'run'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        while (process.poll() is None):
            sleep(0.1)
        print(stdout)
        print(stderr)

    # Threads
    if result[3].get():
        print(runningStr[5])
        process = subprocess.Popen(['sysbench', 'threads', '--thread-locks=1', '--time=20', 'run'],
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE)
        stdout, stderr = process.communicate()
        while (process.poll() is None):
            sleep(0.1)
        print(stdout)
        print(stderr)
    
    window.destroy()

# show the stats of the benchmarks you have done
def showStatsWindow(menuWindow):
    # initialize basic widgets of the window
    menuWindow.destroy()
    statsWindow = ThemedTk(theme=theme)
    statsWindow.title(yourBenchmarksStr)
    statsWindow.geometry(defaultRes)

    #create basic buttons
    createBasicButtons(statsWindow)
    createShowTestButtons(statsWindow)

    # configure the 4 plots to have the same style
    sns.set_style('darkgrid')

def createBasicButtons(window):
    # button to return to the menu
    common.createButton(window, menuStr, lambda: showMenuWindow(window)).place(x=posMenuButton[0],y=posMenuButton[1])
    # button to exit the app
    common.createButton(window, exitStr, lambda: common.quit_program(window)).place(x=posExitButton[0],y=posExitButton[1])

def createShowTestButtons(window):
    common.createButton(window, testStr[0], showCpuTestWindow).place(x=posTestsButton[0],y=posTestsButton[1])
    common.createButton(window, testStr[1], showFileioTestWindow).place(x=posTestsButton[2],y=posTestsButton[3])
    common.createButton(window, testStr[2], showMemoryTestWindow).place(x=posTestsButton[4],y=posTestsButton[5])
    common.createButton(window, testStr[3], showThreadsTestWindow).place(x=posTestsButton[6],y=posTestsButton[7])

def showCpuTestWindow():
    cpuTestData = pd.read_csv(filepath+filenames[0])
    sns.barplot(x=cpuTestData["distribution"], y=cpuTestData["time by event execution"], data=cpuTestData, palette=barplotPalette)
    plt.title(testStr[0])
    plt.show()

def showFileioTestWindow():
    fileioTestData = pd.read_csv(filepath+filenames[1])
    sns.barplot(x=fileioTestData["distribution"], y=fileioTestData["number of operations"], hue=fileioTestData["type of operations"], data=fileioTestData, palette=barplotPalette)
    plt.title(testStr[1])
    plt.show()

def showMemoryTestWindow():
    memoryTestData = pd.read_csv(filepath+filenames[2])
    sns.barplot(x=memoryTestData["distribution"], y=memoryTestData["execution time (s)"], hue=memoryTestData["number of threads"], palette=barplotPalette)
    plt.title(testStr[2])
    plt.show()

    sns.barplot(x=memoryTestData["distribution"], y=memoryTestData["number of operations"], hue=memoryTestData["number of threads"], palette=barplotPalette)
    plt.title(testStr[2])
    plt.show()

def showThreadsTestWindow():
    threadsTestData = pd.read_csv(filepath+filenames[3])
    sns.barplot(x=threadsTestData["distribution"], y=threadsTestData["pre-request stats average (ms)"], hue=threadsTestData["number of threads"], palette=barplotPalette)
    plt.title(testStr[3])
    plt.show()

# main
showMenuWindow(None)