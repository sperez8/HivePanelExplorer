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
    if double == 'True':
        double = True
    else:
        double = False
    hive = Hive(debug = debug, 
                numAxes = axes,
                doubleAxes = double, 
                axisAssignRule = assignment, 
                axisPositRule = position,
                edgePalette = color, 
                #edgeStyleRule = edgeColorRule,
                nodeColor = color
                )
    hive.make_hive(nodefile, edgefile)
    hive.make_debug_file()
    make_html(hiveTitle, hive)
    
    
    
#create window
root  = Tk()
root.title("Hive Plot Maker")
#root.geometry("700x400")

#add a label
app = Frame(root)
row = 0
column = 0
app.grid()
welcome = Label(app, text = "Welcome to Hive Maker!", fg = 'slate blue', font = (fontType, int(fontSize*1.5)))
welcome.grid(row=row, column=column, columnspan = 2)

row += 1
print row
input = Label(app, text = "    Please provide the path to the input files:", fg = 'slate blue', pady = 20, font = (fontType, int(fontSize)))
input.grid(row=row, column=column)
row += 1

#get node and edge file
title = make_entry(app, "Hive Title:", width = 30, row = row, column = column)
row +=1
nodes = make_entry(app, "Nodes:", width = 40, row = row, column = column, bg = 'medium purple')
row += 1 
edges = make_entry(app, "Edges:", width = 40, row = row, column = column, bg = 'medium purple')

#for debugging/development purposes
title.insert(0,"3")
nodes.insert(0,"/Users/sperez/git/HivePlotter/tests/test_nodes_friends.csv")
edges.insert(0,"/Users/sperez/git/HivePlotter/tests/test_edges_friends.csv")

row += 1
input = Label(app, text = "Enter the desired plotting parameters:", fg = 'slate blue', pady = 20, font = (fontType, int(fontSize)))
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
colorOpt = make_options(app2, 'Edge Color:', row = row, column = column, selections = colorOptions)
row += 1

#add button to submit data
b = Button(root)
b.grid(sticky=W+E+N+S)
b.configure(text = "Submit", width=20, command=callback, font = (fontType, int(fontSize)))
    
    
#run gui
root.mainloop()

