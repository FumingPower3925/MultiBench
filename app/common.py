import tkinter as tk
from tkinter import ttk, Canvas
import numpy as n
from subprocess import Popen, PIPE

# initialize common constant variables
menuResolution = '800x400'
defaultResolution = '1920x1200'
menuString = 'Menu'
doBenchmarkString = 'Do a benchmark'
viewStatsString = 'View my stats'
customizeBenchmarkString = 'Customize your benchmark'
yourBenchmarksString = 'Your benchmarks'
exitString = 'Exit'
this_theme = 'arc'
menuButtonx = 1650
menuButtony = 1150
exitButtonx = 1800
exitButtony = 1150
rectangleBgColor = '#7183d3'
rectangleLineColor = '#000000'
posRectangleX1 = 0
posRectangleX2 = 950
posRectangleY1 = 0
posRectangleY2 = 590
widthRectangle = 930
heightRectangle = 570
posLabelX1 = 460
posLabelX2 = 1420
posLabelY1 = 20
posLabelY2 = 610

def createButton(window, txt, func):
    return ttk.Button(
        window,
        text = txt,
        command = func
    )

# using pipes might be a bit outdated, but I think it's useful because it returns the error message
def getFileNames(window):
    p = Popen("ls ./results/*.json", shell=True, stdout=PIPE)
    out, err = p.communicate()
    if p.returncode != 0:
        print(err)
        quit_program(window)
    ret = out.decode("utf-8").split("\n")
    return n.delete(ret, len(ret)-1)

def quit_program(window):
    window.destroy()