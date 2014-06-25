'''
created  18/06/2014

by sperez

Template for GUI
'''

import sys
import os
from gui_uttilities import *
from gui_options import *

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

from hive import Hive
from html_uttilities import *

class HiveGui(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        #create window
        self.title("Hive Plotter GUI")
        
        #add a label
        app = Frame(self)
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
        self.title = make_entry(app, "Hive Title:", width = 50, row = row, column = column, bg = 'aliceblue')
        row +=1
        self.nodes = make_entry(app, "Nodes:", width = 50, row = row, column = column, bg = 'aliceblue')
        row += 1 
        self.edges = make_entry(app, "Edges:", width = 50, row = row, column = column, bg = 'aliceblue')
        
        #for debugging/development purposes
        self.title.insert(0,"hive1")
        self.nodes.insert(0,"/Users/sperez/git/HivePlotter/tests/test_nodes_friends.csv")
        self.edges.insert(0,"/Users/sperez/git/HivePlotter/tests/test_edges_friends.csv")
        
        row += 1
        #add button to update parameters data
        b1 = Button(self)
        b1.grid(row=row, column=column, padx = 10, pady = 30)
        b1.configure(text = "Submit network", width=30, command=self.update, fg = 'blue', font = (fontType, int(fontSize)))
        
        app2 = Frame(self)
        row = 0
        column = 0
        app2.grid()
        
        input = Label(app2, text = "Enter the plotting parameters:", fg = 'slate blue', padx = 10, pady = 30, font = (fontType, int(fontSize)))
        input.grid(row=row, column=column, sticky = S)
        
        #make different option menus
        row += 1
        column = 0
        self.debugOpt, self.debugVar = make_options(app2, 'Debug:', row = row, column = column, selections = debugOptions)
        column += 2
        self.axesOpt, self.axesVar = make_options(app2, 'Number of Axes:', row = row, column = column, selections = axesOptions)
        self.axesVar.set('3')
        column += 2
        self.doubleOpt, self.doubleVar = make_options(app2, 'Double axes:', row = row, column = column, selections = doubleOptions)
        row += 1
        column = 0
        self.assignmentOpt, self.assignmentVar = make_options(app2, 'Node Assignment Rule:', row = row, column = column, selections = assignmentOptions)
        column += 2
        self.positionOpt, self.positionVar = make_options(app2, 'Node Position Rule:', row = row, column = column, selections = positionOptions)
        self.positionVar.set('clustering')
        column += 2
        self.colorOpt, self.colorVar = make_options(app2, 'Default Color:', row = row, column = column, selections = colorOptions)
        row += 1
        column = 0
        self.paletteOpt, self.paletteVar = make_options(app2, 'Edge Color Palette:', row = row, column = column, selections = paletteOptions)
        
        #add button to submit data
        b2 = Button(self)
        b2.grid(sticky=W+E+N+S, padx = 80, pady = 40)
        b2.configure(text = "Create Hive", width=20, command=self.callback, bg = 'aliceblue', font = (fontType, int(fontSize)))
        
    def reset_option_menu(self, w, variable, options, index=None):
        '''reset the values in the option menu

        if index is given, set the value of the menu to
        the option at the given index
        '''
        menu = w["menu"]
        menu.delete(0, "end")
        for string in options:
            menu.add_command(label=string, 
                             command=lambda value=string:
                                  variable.set(value))
        if index is not None:
            variable.set(options[index])
        else:
            variable.set(options[0])
        
        return variable

    def update(self):
        hiveTitle = self.title.get()
        nodefile = self.nodes.get()
        edgefile = self.edges.get()
        
        hive = Hive(debug = False)
        properties = list(hive.get_nodes(nodefile)) + assignmentOptions
        self.assignmentVar = self.reset_option_menu(self.assignmentOpt, self.assignmentVar, properties, index = 2) 
        
        properties = list(hive.get_nodes(nodefile)) + positionOptions
        self.positionVar = self.reset_option_menu(self.positionOpt, self.positionVar, properties) 
    
    
    def callback(self):
        hiveTitle = self.title.get()
        nodefile = self.nodes.get()
        edgefile = self.edges.get()
        debug = self.debugVar.get()
        axes = self.axesVar.get()
        double = self.doubleVar.get()
        assignment = self.assignmentVar.get()
        position = self.positionVar.get()
        color = self.colorVar.get()
        palette = self.paletteVar.get()
        
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
        make_html(hiveTitle, hive)

if __name__ == "__main__":
    app = HiveGui()
    app.mainloop()

