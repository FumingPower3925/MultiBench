import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
import seaborn as sns

# initialize global variables
menuResolution = '800x400'
defaultResolution = '1920x1200'
menuString = 'Menu'
doBenchmarkString = 'Do a benchmark'
viewStatsString = 'View my stats'
customizeBenchmarkString = 'View my stats'
yourBenchmarksString = 'Your benchmarks'
exitString = 'Exit'
theme = 'arc'

# create the menu button
def createMenuButton(window):
    return ttk.Button(
        window,
        text = menuString,
        command = lambda: showMenuWindow(window)
    )

def createBenchmarkButton(window):
    return ttk.Button(
        window,
        text = doBenchmarkString,
        command = lambda: showBenchmarkWindow(window)
    )

def createStatsButton(window):
    return ttk.Button(
        window,
        text = viewStatsString,
        command = lambda: showStatsWindow(window)
    )

def createExitButton(window):
    return ttk.Button(
        window,
        text = exitString,
        command = lambda: quit_program(window)
    )
    
def quit_program(window):
    window.destroy()

# create the widgets in the menu
def showMenuWindow(window):
    if window: window.destroy()

    #main window
    menuWindow = ThemedTk(theme=theme)
    menuWindow.title(menuString)
    menuWindow.geometry(menuResolution)

    createBenchmarkButton(menuWindow).place(x=150,y=100)
    createStatsButton(menuWindow).place(x=500,y=100)
    createExitButton(menuWindow).place(x=665,y=350)

    menuWindow.mainloop()

# button that goes to the benchmarks page
def showBenchmarkWindow(menuWindow):
    menuWindow.destroy()
    #window to do the benchmarks
    benchmarkWindow = tk.Tk()
    benchmarkWindow.title(customizeBenchmarkString)
    benchmarkWindow.geometry(defaultResolution)

    menuButton = createMenuButton(benchmarkWindow)
    menuButton.pack()

# button that goes to the stats of your benchmarks
def showStatsWindow(menuWindow):
    menuWindow.destroy()
    #window to see your benchmarks' stats
    statsWindow = tk.Tk()
    statsWindow.title(yourBenchmarksString)
    statsWindow.geometry(defaultResolution)

    menuButton = createMenuButton(statsWindow)
    menuButton.pack()

# main
showMenuWindow(None)