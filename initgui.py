# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 19:16:38 2020

@author: Mikko
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

#root = Tk()
#root.filename =  filedialog.asksaveasfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
#print (root.filename)


def get_filename_dialog(root):
    root.filename =  filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("jpeg files","*.jpg"),("all files","*.*")))
    return(root.filename)
    
class AppGUI:
    
    def __init__(self, root, windowsize):
        
        
        self.root = root
        _tabs = ttk.Notebook(root, width=900, height=900)
        
        leaf = Frame(_tabs)
        _tabs.add(leaf, text="Create animation")
        
        self.windowsize = windowsize
        
        self.xpic,self.ypic = 0,0
        self.root.bind("<B1-Motion>", self.callback)
        self.root.bind("<Button-1>", self.callback)
        
        _f1 = Frame(leaf)
        _f1.pack(fill=BOTH)
        
        f1 = Frame(_f1)
        f1.pack(fill=BOTH)
        
        self.photoframe = Frame(f1)
        
        getfilebtn = Button(f1, width=15, text="Get picture file", command=self.get_picture)
        getfilebtn.pack(side=LEFT)
        
        createbtn = Button(f1, width=15, text="Execute", command=self.create)
        createbtn.pack(side=LEFT)
        
        defaultsbtn = Button(f1, width=15, text="Set defaults", command=self.set_defaults)
        defaultsbtn.pack(side=LEFT) 
        
        clearbtn =  Button(f1, width=15, text="Clear rows", command=self.clear_rows)
        clearbtn.pack(side=LEFT)
    
        f2 = Frame(_f1)
        f2.pack(side=TOP)
        
        self.fnamevar = StringVar()
        
        self.filename = Label(f2, textvariable=self.fnamevar)
        self.filename.pack(side=TOP)
        
        addrow = Button(f2, width=15, text="Add row", command=self.set_option_row)
        addrow.pack(side=BOTTOM)
        
        self.rows = Frame(_f1, borderwidth=2)
        self.rows.pack(side=TOP)
        
        self.row_frames = []
        self.rows_empty = True
        
        #s1 = ttk.Separator(_f1, orient="horizontal")
        #s2 = ttk.Separator(_f1, orient="horizontal")
        
        self.index = 0
        self.arr_loaded = False
        self.checkvars = []
        
        _f2 = Frame(_tabs)
        _tabs.add(_f2, text="Preview")
        
        _tabs.grid(row=0, column=0)
        
    def callback(self, event):
        pass
    
    def set_option_row(self):
        
        row = Frame(self.rows)
        row.pack(side=TOP)
        
        radlabel = Label(row, text="shift length",height=1, compound=LEFT)
        radlabel.pack(side=LEFT)
        
        var = IntVar()
        
        cneg = Checkbutton(row, text="negative", variable=var)
        cneg.pack(side=LEFT)
        
        self.checkvars.append(var)
         
        radius = tk.Scale(row, orient=tk.HORIZONTAL, length=200)
        radius.pack(side=LEFT)
        radius.set(25)
        
        combolabel = Label(row, text="# Channel",height=1, compound=LEFT)
        combolabel.pack(side=LEFT)
        
        channels = ttk.Combobox(row, values=[str(i) for i in range(3)])
        channels.pack(side=LEFT)
        channels.set(0)
        
        self.row_frames.append(row)
        
        self.rows_empty = False
       
    def get_picture(self):
        photo_name = get_filename_dialog(self.root)
        self.fnamevar.set(photo_name)
        load = Image.open(photo_name)
        self.arr = to_array(load)
        self.arr_loaded = True
   
    def get_row_parameters(self):
        self.parameters = []
        
        i = 0
        for fra in self.row_frames:
            rowwid = [widget for widget in fra.winfo_children()]
            self.parameters.append((self.checkvars[i].get(),rowwid[2].get(),int(rowwid[4].get())))
            i += 1
            del rowwid
            
    def save_parameters(self):
        pass
    
    def load_parameters(self):
        pass
            
    def clear_rows(self):
        for widget in self.rows.winfo_children():
            widget.destroy()
            
        self.row_frames = []
        self.parameters = []
        self.checkvars = []
        self.rows_empty=True
    
    def set_defaults(self):
        pass
    
    def create(self):
        if not self.rows_empty:
            self.get_row_parameters()
            print(self.parameters)
            
            if self.arr_loaded:
                self.animation = Animate1(self.arr)
                for par in self.parameters:
                    p1,p2,p3 = par
                    sign = [1,-1][p1]
                    self.animation.create_cycle1(maxshift=p2*sign, channel=p3)
                self.animation.stack_cycles()
                
                print("starting")
                self.animation.history_to_gif(counter=int(time.time()))   
                print("done")

if True:
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
        