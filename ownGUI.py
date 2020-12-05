# Developed by Thomas To
# Undergraduate Researcher
# Dec 5 2020

from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import cv2
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.animation as animation
from matplotlib import style
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib import pyplot as plt

# The idea is to use Tkinter as a user back end to update the matplotlib
img_gs = cv2.imread('img.tif', cv2.IMREAD_GRAYSCALE)

# Initiating & Reset values of thresholds
global minCannVal0, maxCannyVal0
minCannyVal0 = 0
maxCannyVal0 = 0

newMinCannyVal, newMaxCannyVal = 0,0

class ownGUI:
    def __init__(self, master):      
        # Create a container
        frame = tk.Frame(master)
        
        # Create event manipulator/caller here
        self.xLabel = Label(frame, text="Canny Edge Minimum Threshold").pack()
        self.minVal = tk.Scale(frame, from_=-100, to=100,
                               sliderlength = 15, length = 250, resolution = 1,
                               command=self.update_minVal, orient=HORIZONTAL).pack()
            
        self.maxLabel = Label(frame, text="Canny Edge Maximum Threshold").pack()
        self.maxVal = tk.Scale(frame, from_=-100, to =100,
                               sliderlength = 15, length = 250, resolution = 1,
                               command=self.update_maxVal, orient=HORIZONTAL).pack()
        
        # Create button to export 
        self.export = Button(frame,
                             text = 'Export',
                             command=self.exportFigure
                            ).pack()
        # (initiate) Figures
        fig = Figure(tight_layout=True)
        plotOrig = fig.add_subplot(1,2,1)

        global plotEdges
        plotEdges = fig.add_subplot(1,2,2)
        
        plotOrig.imshow(img_gs)

        plotOrig.set_title("Original Image")
        
        plotEdges.set_title("Edged Image")
        # "meta-data" to draw on
        self.canvas = FigureCanvasTkAgg(fig, master = master)
        self.canvas.draw() #init meta graph; clear, update and draw in methods
        self.canvas.get_tk_widget().pack(side='top',fill='both',expand=1)

        frame.pack() # show

    def update_minVal(self, newMin):
        global newMinCannyVal, newMaxCannyVal, showEdges
        
        newMinCannyVal = minCannyVal0 + int(newMin)
        self.showEdges = ownGUI.quantifyData(newMinCannyVal, newMaxCannyVal)
        
        plotEdges.imshow(self.showEdges)

        self.canvas.draw()   
        
    def update_maxVal(self, newMax):
        global newMinCannyVal, newMaxCannyVal, showEdges

        newMaxCannyVal = maxCannyVal0 + int(newMax)
        
        self.showEdges = ownGUI.quantifyData(newMinCannyVal, newMaxCannyVal)
        
        plotEdges.imshow(self.showEdges)

        self.canvas.draw()         
        
    def quantifyData(minVal, maxVal):
        minCannyVal = minVal
        maxCannyVal = maxVal
        edges = cv2.Canny(img_gs, minCannyVal, maxCannyVal)
        thresh = cv2.threshold(edges, 0, 255,cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

        # Close Contour
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (7,7))
        close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=1)
        
        # Find outer contour and fill with white
        cnts = cv2.findContours(close, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        filledEdges = cv2.fillPoly(close, cnts, [255,255,255])
        return filledEdges
    
    def exportFigure(self):
        cv2.imwrite('img_Canny.tif', self.showEdges)
        

root = Tk()
gui = ownGUI(root)
root.mainloop()


