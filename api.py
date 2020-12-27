# -*- coding: utf-8 -*-
"""
Created on Wed Sep  9 19:16:38 2020

@author: Mikko
"""

import numpy as np
import time

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

import multiprocessing as mp

def limit_cpu_usage():
    pass



def to_image(arr, path):
    im = PIL.Image.fromarray(np.uint8(arr))        
    #render = ImageTk.PhotoImage(im)
    im.save((path))
    
def to_array(photo):
    I = np.asarray(photo)
    return(I)
    
def remove_channel(arr, channel=0, ratio=0.0):
    arr2 = arr.copy()
    arr2[:,:,channel] = arr2[:,:,channel]*ratio
    return(arr2)    
    
    
def shade_divide(arr, lim=128, color1=[255,255,255], color2=[0,0,0]):
    """returns a picture array divided into two colors cells from input pic 
    depending on color average limit (lim).
    shape of returned array is the same as input array"""
    
    averages = np.sum(arr,axis=2)/3
    averages = averages.astype(int)
    w = np.where(averages>lim)
    
    divided = np.array([np.ones(arr.shape[0:2])*color2[k] for k in range(arr.shape[2])])
    divided = np.moveaxis(divided, 0, -1)
    
    arrw = np.array(w)
    #return(arrw)
    
    for row in range(arrw.shape[1]):
        i,j = arrw[:,row]
        divided[i,j] = np.array(color1)
    
    divided = divided.astype(int)
    
    return(divided)
 
#s = shade_divide(arr,100,[0,127,255],[255,255,255])
#show(s)

def shift_picture(arr, direction=[0,1], npixels=100, atrows=[0,1.0]):
    
    "returns a picture that is shifted into given direction (direction) by given amount of pixels"
    #axes = [arr.shape[i] for i in direction]
    axes = [s for s in arr.shape]
    
    fromrow,torow = int(axes[1]*atrows[0]),int(axes[1]*atrows[1])
    
    shifted = arr.copy()
    
    if direction[1]!=0:
        for line in range(fromrow,torow):
            try:
                shifted[:,line,:] = arr[:,line+npixels*direction[1],:] 
            except:
                continue
            
    if direction[0]!=0:
        fromrow,torow = int(axes[0]*atrows[0]),int(axes[0]*atrows[1])
        for line in range(fromrow,torow):
            try:
                shifted[line,:,:] = shifted[line+npixels*direction[0],:,:] 
            except:
                continue
        
    
    return(shifted)

def half_image(arr1, arr2, ratio=0.5):
    "colliding two images into one by a ratio"
    half_arr = (arr1*ratio+arr2*(1-ratio)).astype(int)
    return(half_arr)
    
def stack_images(arrays,ratios=[]):
    "stacking multiple image arrays into one average"
    if ratios==[]:
        ratios = [0.5 for i in range(len(arrays))]
        
    stacked_arr = arrays[0]    
    
    for i in range(1,len(arrays)):
        stacked_arr = half_image(stacked_arr,arrays[i],ratios[i-1])
        
    return(stacked_arr)
    

class Animation1:
    
    def __init__(self, base_pic, history=[]):
        self.base_pic = base_pic
        self.history = history
        self.cycles=[]
        self.n_frames = 0
            
    def tweener(self, start, end, n_between=10):
        pass
        
    def color_shift(self):
        pass
            
    def create_cycle1(self, nsteps=25, maxshift=100, channel=0, back=True, shiftdir=[0,1]):
        arr = self.base_pic.copy()
        cycle = []
            
        for istep in range(nsteps):
            ratio = istep/nsteps
            dropped = remove_channel(arr,channel,(1.0-ratio))
            shift = int((ratio)*maxshift)
            shifted = shift_picture(dropped,npixels=shift,direction=shiftdir)
            halfed = half_image(arr,shifted)
                
            cycle.append(halfed)
                
        l = len(cycle)
        if back:
            for i in range(1,l):
                try:
                    cycle.append(cycle[l-i])
                except IndexError:
                    print(l-i)
               
            #self.history = cycle
        if len(cycle)>self.n_frames:
            self.n_frames=len(cycle)
            
        self.cycles.append(cycle)
            
    def combine_cycles(self,i1,i2):
        c1,c2 = self.cycles[i1],self.cycles[i2]
        combined = []
        i = 0
        for arr in c1:
            combined.append(half_image(arr,c2[i]))
            i += 1
        self.history = combined
            
    def stack_cycles(self):
        "stacks all cycles of self into one"
        stacked = []
        for i1 in range(self.n_frames):
            stacked_arrays = []
            for i2 in range(len(self.cycles)):
                try:
                    stacked_arrays.append(self.cycles[i2][i1])    
                except:
                    continue
            stacked.append(stack_images(stacked_arrays))
        self.history = stacked   
                    
    def history_to_gif(self, name='png_to_gif', counter=1, dur=100, cycles=1):
        "saves self history into on gif animation into home directory"
        frames = []
            
        for c in range(cycles):
            for f in self.history:
                im = PIL.Image.fromarray(np.uint8(f))
                frames.append(im)
            
        frames[0].save('{}_{}.gif'.format(name,counter), format="GIF",
                append_images=frames[1:],
                save_all=True,
                duration=dur, loop=0)
            

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
                self.animation = Animation1(self.arr)
                for par in self.parameters:
                    p1,p2,p3 = par
                    sign = [1,-1][p1]
                    self.animation.create_cycle1(maxshift=p2*sign, channel=p3)
                self.animation.stack_cycles()
                
                print("starting")
                self.animation.history_to_gif(counter=int(time.time()))   
                print("done")


 
