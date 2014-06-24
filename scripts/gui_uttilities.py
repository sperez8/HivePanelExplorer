'''
created  20/06/2014

by sperez

all the functions we need in the gui
to make labels, option menus, etc...
'''

from Tkinter import *

fontType = 'Helvetica'
fontSize = 16

    
def make_entry(parent, caption, width=None, row = 0, column = 0, **options):
    Label(parent, text=caption, font = (fontType, int(fontSize))).grid(row=row, column=column)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.grid(row=row, column=column+1, padx = 15)
    return entry

def make_options(parent, caption, row = 0, column = 0, selections = [], **options):
    Label(parent, text=caption, font = (fontType, int(fontSize))).grid(row=row, column=column)
    var = StringVar(parent)
    var.set(selections[0]) #default value
    w = apply(OptionMenu, (parent, var) + tuple(selections))
    w.grid(row=row, column=column+1, sticky=W)
    return var