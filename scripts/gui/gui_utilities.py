'''
created  20/06/2014

by sperez

all the functions we need in the gui
to make labels, option menus, etc...
'''
import os
import sys
from Tkinter import *
import tkFileDialog
from gui_options import colors

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

from hive import Hive
from graph_utilities import *

ACCEPTED_FILETYPES = (("CSV files", "*.csv"),("Tab delimited files", "*.txt"))
FONT_TYPE = 'Helvetica'
FONT_SIZE = 12
TEXT_ENTRY_WIDTH = 60
MENU_WIDTH = 13
PADDING = int(FONT_SIZE*0.3)

    
def make_entry(parent, caption, width=None, row = 0, column = 0, **options):
    Label(parent, text=caption, font = (FONT_TYPE, int(FONT_SIZE))).grid(row=row, column=column, sticky = E, ipadx = PADDING*2)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.grid(row=row, column=column+1, padx = PADDING)
    return entry

def make_options(parent, caption, row = 0, column = 0, selections = [], width = MENU_WIDTH, command = None, **options):
    label = Label(parent, text=caption, font = (FONT_TYPE, int(FONT_SIZE*0.9)))
    label.grid(row=row, column=column, sticky=W)
    var = StringVar(parent)    
    var.set(selections[0]) #default value   
    w = apply(OptionMenu, (parent, var) + tuple(selections))
    w.configure(width = width)
    if command:
        var.trace('w',command) 
    w.grid(row=row, column=column+1, sticky=W, padx = PADDING)
    return w,var

def get_num_colors(edges, style):
    if style == 'uniform':
        colors = [1]
    else:
        edgefile = edges.get()
        hive = Hive(debug = True)
        properties = hive.get_edges(edgefile)[style]
        categories = find_categories(properties)
        if categories:
            colors = [len(categories)]
        else:
            colors = [i for i in range(1,10)]
    return colors

def get_palette(hue,number):
    if hue in colors.keys():
        return colors[hue][:number]
    else:
        print "Desired hue not found. Defaulted to blue palette"
        return colors['blue'][:number]