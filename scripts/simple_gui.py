'''
created  18/06/2014

by sperez

Template for GUI
'''

import sys
import os
from Tkinter import *
from main import *
from gui_options import *

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

from tests.test_parameter_friends import *

#create window
root  = Tk()
root.title("Hive Plot Maker")
root.geometry("600x400")

#some functions we might need
def callback():
    hiveTitle = title.get()
    nodefile = nodes.get()
    edgefile = edges.get()
    debug = debugOpt.get()
    assignment = assignmentOpt.get()
    position = positionOpt.get()
    color = colorOpt.get()
    hive = make_hive(nodefile, edgefile, debug, 
                        #numAxes = numAxes,
                        #doubleAxes = doubleAxes, 
                        axisAssignRule = assignment, 
                        axisPositRule = position, 
                        #edgePalette = edgeColorPalette, 
                        #edgeStyleRule = edgeColorRule
                        )
    make_html(hiveTitle, hive)
    
def make_entry(parent, caption, width=None, **options):
    Label(parent, text=caption).pack(side=LEFT)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.pack()
    return entry

def make_options(parent, options):
    var = StringVar(parent)
    var.set(options[0]) #default value
    w = apply(OptionMenu, (parent, var) + tuple(options))
    w.pack()
    return var

#add a label
app = Frame(root)
app.pack()
welcome = Label(app, text = "Welcome to Hive Maker!")
welcome.pack()

#get node and edge file
title = make_entry(app, "Hive Title:", 30)
nodes = make_entry(app, "Nodes:", 60)
edges = make_entry(app, "Edges:", 60)

#make different option menus
debugOpt = make_options(app, debugOptions)
assignmentOpt = make_options(app, assignmentOptions)
positionOpt = make_options(app, positionOptions)
colorOpt = make_options(app, colorOptions)

#add button to submit data
b = Button(root)
b.pack()
b.configure(text = "Submit", width=20, command=callback)

#run gui
root.mainloop()
