"""
Created on Wed Sep  9 19:16:38 2020

@author: Mikko
"""

from tkinter import *
from splits import *


"""
from tkinter import filedialog
from tkinter import *


from tkinter import Frame, Canvas, Label, Button, LEFT, RIGHT, ALL, Tk, Entry, BOTH, S
from random import randint
import tkinter as tk
from tkinter import ttk
import numpy as np

from PIL import Image, ImageTk
import PIL

import time
"""


#import initgui

start = input("pop gui? \n")
if start:
    window = Tk()
    window.title("...")
    
    lx,ly = 900,900
    size = "{}x{}".format(lx,ly)
    window.geometry(size)
    window.resizable(0, 1) 

    framex,framey = 900,900
    gui1 = AppGUI(window, windowsize=(framex,framey))
    #gui2 = App2(root)
    window.mainloop()
        
