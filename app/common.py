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
posMenuButton = [1650,1150]
posExitButton = [1800,1150]
rectangleBgColor = '#7183d3'
rectangleLineColor = '#000000'
filenames = ['results_cpuTest.csv','results_fileioTest.csv','results_memoryTest.csv','results_threadsTest.csv']
testString = ['CPU Test','FileIO Test','Memory Test','Threads Test']
posTestsButton = [640,400,1260,400,640,800,1260,800]
barplotPalette = 'bright'

def createButton(window, txt, func):
    return ttk.Button(
        window,
        text = txt,
        command = func
    )

def quit_program(window):
    window.destroy()