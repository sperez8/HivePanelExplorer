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
from graph_uttilities import *

class HiveGui(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        #create window
        self.title("Hive Plotter GUI")
        self.loaded = False
        #add a label
        app = Frame(self)
        row = 0
        column = 0
        app.grid()
        welcome = Label(app, text = "Welcome to Hive Plotter!", fg = 'slate blue', font = (fontType, int(fontSize*1.5)))
        welcome.grid(row=row, column=column, columnspan = 2)
        
        row += 1
        input = Label(app, text = "Please provide the path to the input files:", fg = 'slate blue', font = (fontType, int(fontSize)))
        input.grid(row=row, column=column, padx = 10, pady = 30, sticky = W)
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
        
        input = Label(app2, text = "Enter the plotting parameters:", fg = 'slate blue', font = (fontType, int(fontSize)))
        input.grid(row=row, column=column, padx = 20, pady = 30, sticky = W)
        
        #make different option menus
        row += 1
        column = 0
        self.debugOpt, self.debugVar = make_options(app2, 'Debug:', row = row, column = column, selections = debugOptions)
        column += 2
        self.axesOpt, self.axesVar = make_options(app2, 'Number of Axes:', row = row, column = column, selections = axesOptions)
        self.axesVar.set('3')
        column += 2
        self.doubleOpt, self.doubleVar = make_options(app2, 'Double axes:', row = row, column = column, selections = doubleOptions)
        self.doubleVar.set('False')
        row += 1
        column = 0
        self.assignmentOpt, self.assignmentVar = make_options(app2, 'Node Assignment Rule:', row = row, column = column, selections = assignmentOptions)
        column += 2
        self.positionOpt, self.positionVar = make_options(app2, 'Node Position Rule:', row = row, column = column, selections = positionOptions)
        self.positionVar.set('clustering')
        row += 1
        column = 0
        self.edgeStyleOpt, self.edgeStyleVar = make_options(app2, 'Edge Style Rule:', row = row, column = column, selections = edgeStyleOptions)
        
        #add button to submit parameters
        b2 = Button(self)
        b2.grid(padx = 10, pady = 40, columnspan = 2)
        b2.configure(text = "Load parameters", width=20, command=self.load_parameters, bg = 'aliceblue', font = (fontType, int(fontSize)))


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

    def load_parameters(self):
        #create some optional parameters for some styling
        app3 = Frame(self)
        row = 0
        column = 0
        app3.grid()
        
        style = self.edgeStyleVar.get()
        if style == 'uniform':
            colors = colorOptions
        
        else:
            edgefile = self.edges.get()
            hive = Hive(debug = True)
            properties = hive.get_edges(edgefile)[style]
            categories = find_categories(properties)
            if categories:
                colors = ''
                for c in colorOptions[0:len(categories)]:
                    colors += ' ' + c
                colors = [colors]
        
            else:
                colors = [0,1,2,3,4,5]
        
        if self.loaded:
            self.colorVar = self.reset_option_menu(self.colorOpt, self.colorVar, colors)
        else:
            input = Label(app3, text = "Change the node and edge coloring:", fg = 'slate blue', font = (fontType, int(fontSize)))
            input.grid(row=row, column=column, padx = 20, pady = 30, sticky = W)
            row += 1
            self.colorOpt, self.colorVar = make_options(app3, 'Edge Color Palette:', row = row, column = column, selections = colors)
            column += 2
            self.nodeColorOpt, self.nodeColorVar = make_options(app3, 'Node Color:', row = row, column = column, selections = colorOptions)
            
            #add button to create hive
            b2 = Button(app3)
            b2.grid(padx = 80, pady = 40, columnspan = 4)
            b2.configure(text = "Create Hive", width=80, command=self.callback, bg = 'aliceblue', font = (fontType, int(fontSize)))
            
        self.loaded = True

    def update(self):
        nodefile = self.nodes.get()
        edgefile = self.edges.get()
        
        hive = Hive(debug = False)
        properties = list(hive.get_nodes(nodefile).keys()) + assignmentOptions
        self.assignmentVar = self.reset_option_menu(self.assignmentOpt, self.assignmentVar, properties, index = 2) 
        
        properties = list(hive.get_nodes(nodefile).keys()) + positionOptions
        self.positionVar = self.reset_option_menu(self.positionOpt, self.positionVar, properties) 

        properties = list(hive.get_edges(edgefile)) + edgeStyleOptions
        self.edgeStyleVar = self.reset_option_menu(self.edgeStyleOpt, self.edgeStyleVar, properties)
    
    def callback(self):
        hiveTitle = self.title.get()
        nodefile = self.nodes.get()
        edgefile = self.edges.get()
        debug = self.debugVar.get()
        axes = self.axesVar.get()
        double = self.doubleVar.get()
        assignment = self.assignmentVar.get()
        position = self.positionVar.get()
        edgeColor = self.colorVar.get()
        edgeStyle = self.edgeStyleVar.get()
        nodeColor = self.nodeColorVar.get()
        
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
        
        if edgeStyle == 'uniform':
            edgeStyle = None
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
                    edgePalette = edgeColor, 
                    edgeStyleRule = edgeStyle,
                    nodeColor = nodeColor
                    )
        hive.make_hive(nodefile, edgefile)
        make_html(hiveTitle, hive)

if __name__ == "__main__":
    app = HiveGui()
    app.mainloop()

