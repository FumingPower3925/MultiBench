import tkinter as tk
from tkinter import ttk, Canvas
from ttkthemes import ThemedTk
import seaborn as sns
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
defaultRes = common.defaultResolution
menuButtonX = common.menuButtonx
menuButtonY = common.menuButtony
exitButtonX = common.exitButtonx
exitButtonY = common.exitButtony
rectangleBgCol = common.rectangleBgColor
rectangleLineCol = common.rectangleLineColor

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
    # create rectangles
    common.createRectangles(benchmarkWindow)

# show the stats of the benchmarks you have done
def showStatsWindow(menuWindow):
    # initialize basic widgets of the window
    menuWindow.destroy()
    statsWindow = tk.Tk()
    statsWindow.title(yourBenchmarksStr)
    statsWindow.geometry(defaultRes)

    #create basic buttons
    createBasicButtons(statsWindow)
    # rectangles for fileoTest, cpuTest, threadsTest and memoryTest respectively
    common.createRectangles(statsWindow)

    # get the names of all the files with stats and read them. we remove the last position because i'ts a \n
    files = common.getFileNames(statsWindow)

    for filename in files:
        # default is read-only, no need to specify opening mode
        file = open(filename)
        data = json.load(file)
        

        file.close()  

def createBasicButtons(window):
    # button to return to the menu
    common.createButton(window, menuStr, lambda: showMenuWindow(window)).place(x=menuButtonX,y=menuButtonY)
    # button to exit the app
    common.createButton(window, exitStr, lambda: common.quit_program(window)).place(x=exitButtonX,y=exitButtonY)

# main
showMenuWindow(None)