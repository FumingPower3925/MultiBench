# graphic design
import tkinter as tk
from tkinter import ttk, Canvas
from ttkthemes import ThemedTk
# show stats
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import json
import common

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
rectangleBgCol = common.rectangleBgColor
rectangleLineCol = common.rectangleLineColor
testStr = common.testString
posTestsButton = common.posTestsButton
barplotPalette = common.barplotPalette

# create the widgets in the menu
def showMenuWindow(window):
    if window: window.destroy()

    #main window
    menuWindow = ThemedTk(theme=theme)
    menuWindow.title(menuStr)
    menuWindow.geometry(menuRes)

    # create a square to make it look good
    w = Canvas(menuWindow, width=775, height=375)
    w.create_rectangle(12.5, 12.5, 787.5, 387.5, fill=rectangleBgCol, outline = rectangleLineCol)
    w.place(x=12.5, y=12.5)

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
    benchmarkWindow = tk.Tk()
    benchmarkWindow.title(customizeBenchmarkStr)
    benchmarkWindow.geometry(defaultRes)

    #create basic buttons
    createBasicButtons(benchmarkWindow)

# show the stats of the benchmarks you have done
def showStatsWindow(menuWindow):
    # initialize basic widgets of the window
    menuWindow.destroy()
    statsWindow = tk.Tk()
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
    cpuTestData = pd.read_csv('results/results_cpuTest.csv')
    sns.barplot(x=cpuTestData["distribution"], y=cpuTestData["time by event execution"], data=cpuTestData, palette=barplotPalette)
    plt.title(testStr[0])
    plt.show()

def showFileioTestWindow():
    fileioTestData = pd.read_csv('results/results_fileioTest.csv')
    sns.barplot(x=fileioTestData["distribution"], y=fileioTestData["number of operations"], hue=fileioTestData["type of operations"], data=fileioTestData, palette=barplotPalette)
    plt.title(testStr[1])
    plt.show()

def showMemoryTestWindow():
    memoryTestData = pd.read_csv('results/results_memoryTest.csv')
    sns.barplot(x=memoryTestData["distribution"], y=memoryTestData["execution time (s)"], palette=barplotPalette)
    plt.title(testStr[2])
    plt.show()

    sns.barplot(x=memoryTestData["distribution"], y=memoryTestData["number of operations"], palette=barplotPalette)
    plt.title(testStr[2])
    plt.show()

def showThreadsTestWindow():
    threadsTestData = pd.read_csv('results/results_threadsTest.csv')
    sns.barplot(x=threadsTestData["distribution"], y=threadsTestData["pre-request stats average (ms)"], palette=barplotPalette)
    plt.title(testStr[3])
    plt.show()

# main
showMenuWindow(None)