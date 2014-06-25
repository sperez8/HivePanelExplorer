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
    palette = paletteOpt.get()
    
    #convert types
    axes = int(axes)
    
    if debug == 'True':
        debug = True
    else: 
        debug = False
    
    if double == 'True':
        double = True
    else:
        double = False
    
    if palette == 'None':
        palette = None  
    else: 
        try:
            palette = int(palette)   
        except:
            pass
    
    hive = Hive(debug = debug, 
                numAxes = axes,
                doubleAxes = double, 
                axisAssignRule = assignment, 
                axisPositRule = position,
                edgePalette = color, 
                edgeStyleRule = palette,
                nodeColor = color
                )
    hive.make_hive(nodefile, edgefile)
    hive.make_debug_file()
    make_html(hiveTitle, hive)
    
    
    
#create window
root  = Tk()
root.title("Hive Plotter GUI")
#root.geometry("700x400")

#add a label
app = Frame(root)
row = 0
column = 0
app.grid()
welcome = Label(app, text = "Welcome to Hive Plotter!", fg = 'slate blue', font = (fontType, int(fontSize*1.5)))
welcome.grid(row=row, column=column, columnspan = 2)

row += 1
input = Label(app, text = "    Please provide the path to the input files:", fg = 'slate blue', pady = 20, font = (fontType, int(fontSize)))
input.grid(row=row, column=column)
row += 1

#get node and edge file
title = make_entry(app, "Hive Title:", width = 50, row = row, column = column, bg = 'aliceblue')
row +=1
nodes = make_entry(app, "Nodes:", width = 50, row = row, column = column, bg = 'aliceblue')
row += 1 
edges = make_entry(app, "Edges:", width = 50, row = row, column = column, bg = 'aliceblue')

#for debugging/development purposes
title.insert(0,"hive1")
nodes.insert(0,"/Users/sperez/git/HivePlotter/tests/test_nodes_friends.csv")
edges.insert(0,"/Users/sperez/git/HivePlotter/tests/test_edges_friends.csv")

row += 1
input = Label(app, text = "Enter the desired plotting parameters:", fg = 'slate blue', pady = 30, font = (fontType, int(fontSize)))
input.grid(row=row, column=column)

app2 = Frame(root)
row = 0
column = 0
app2.grid()

#make different option menus
row += 1
column = 0
debugOpt = make_options(app2, 'Debug:', row = row, column = column, selections = debugOptions)
column += 2
axesOpt = make_options(app2, 'Number of Axes:', row = row, column = column, selections = axesOptions)
column += 2
doubleOpt = make_options(app2, 'Double axes:', row = row, column = column, selections = doubleOptions)
row += 1
column = 0
assignmentOpt = make_options(app2, 'Node Assignment Rule:', row = row, column = column, selections = assignmentOptions)
column += 2
positionOpt = make_options(app2, 'Node Position Rule:', row = row, column = column, selections = positionOptions)
column += 2
colorOpt = make_options(app2, 'Default Color:', row = row, column = column, selections = colorOptions)
row += 1
column = 0
paletteOpt = make_options(app2, 'Edge Color Palette:', row = row, column = column, selections = paletteOptions)

#add button to submit data
b = Button(root)
b.grid(sticky=W+E+N+S, padx = 80, pady = 40)
b.configure(text = "Submit", width=20, command=callback, font = (fontType, int(fontSize)))
    
    
#run gui
root.mainloop()

