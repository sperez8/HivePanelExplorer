'''
created  18/06/2014

by sperez

Template for GUI
'''

import sys
import os
from gui_uttilities import *
from gui_options import *
from hive import Hive
from html_uttilities import *

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

from tests.test_parameter_friends import *


def callback():
    hiveTitle = title.get()
    nodefile = nodes.get()
    edgefile = edges.get()
    debug = debugOpt.get()
    axes = axesOpt.get()
    double = doubleOpt.get()
    assignment = assignmentOpt.get()
    position = positionOpt.get()
    color = colorOpt.get()
    
    #convert types
    debug = bool(debug)
    axes = int(axes)
    double = bool(double)
    
    hive = Hive(debug = debug, 
                numAxes = axes,
                doubleAxes = double, 
                axisAssignRule = assignment, 
                axisPositRule = position,
                #edgePalette = edgeColorPalette, 
                #edgeStyleRule = edgeColorRule,
                color = color
                )
    hive.make_hive(nodefile, edgefile)
    make_html(hiveTitle, hive)
    
    
    
#create window
root  = Tk()
root.title("Hive Plot Maker")
#root.geometry("700x400")

#add a label
app = Frame(root)
app.pack()
welcome = Label(app, text = "Welcome to Hive Maker!")
welcome.pack()

#get node and edge file
title = make_entry(app, "Hive Title:", 30) #side = 'left')
nodes = make_entry(app, "Nodes:", 60, fill = True, bg = 'purple')
edges = make_entry(app, "Edges:", 60, fill = True, bg = 'purple')

#make different option menus
debugOpt = make_options(app, 'debug:', debugOptions)
axesOpt = make_options(app, 'Number of Axes:', axesOptions)
doubleOpt = make_options(app, 'Double axes?:', doubleOptions)
assignmentOpt = make_options(app, 'Node Assignment Rule:', assignmentOptions)
positionOpt = make_options(app, 'Node Position Rule:', positionOptions)
colorOpt = make_options(app, 'color:', colorOptions)

#add button to submit data
b = Button(root)
b.pack()
b.configure(text = "Submit", width=20, command=callback)

#run gui
root.mainloop()
