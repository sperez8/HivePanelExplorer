'''
created  20/06/2014

by sperez

all the functions we need in the gui
to make labels, option menus, etc...
'''

from Tkinter import *
from gui_options import colors

fontType = 'Helvetica'
fontSize = 16

    
def make_entry(parent, caption, width=None, row = 0, column = 0, **options):
    Label(parent, text=caption, font = (fontType, int(fontSize))).grid(row=row, column=column, sticky = E, ipadx = 20)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.grid(row=row, column=column+1, padx = 15)
    return entry

def make_options(parent, caption, row = 0, column = 0, selections = [], **options):
    label = Label(parent, text=caption, font = (fontType, int(fontSize*0.9)))
    label.grid(row=row, column=column, sticky=W)
    var = StringVar(parent)
    var.set(selections[0]) #default value
    w = apply(OptionMenu, (parent, var) + tuple(selections))
    w.grid(row=row, column=column+1, sticky=W, padx = 8)
    return w,var

def get_palette(hue,number):
    if hue in colors.keys():        
        
        return colors[hue][:number]
    else:
        print "Desired hue not found. Defaulted to blue palette"
        return colors['blue'][:number]