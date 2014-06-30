'''
created  18/06/2014

by sperez

Template for GUI
'''

import sys
import os
import webbrowser
from gui_uttilities import *
from gui_options import *

_cur_dir = os.path.dirname(os.path.realpath(__file__))
_root_dir = os.path.dirname(_cur_dir)
sys.path.insert(0, _root_dir)

from hive import Hive
from html_uttilities import *
from graph_uttilities import *

_root_dir = os.path.dirname(_root_dir)
NODES = _root_dir + "/tests/test_nodes_friends.csv"
EDGES = _root_dir + "/tests/test_edges_friends.csv"

class HiveGui(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs)
        #create window
        self.title("Hive Plotter GUI")
        self.loaded = False
        
        self.minsize(300,300)
        self.geometry("930x750")
        
        self.app = Frame(self)
        
        row = 0
        column = 0
        self.app.grid()        
        
        welcome = Label(self.app, text = "Welcome to Hive Plotter", fg = 'slate blue', font = (FONT_TYPE, int(FONT_SIZE*1.5)))
        welcome.grid(row=row, column=column, columnspan = 2, pady = PADDING*2)
        
        row += 1
        input = Label(self.app, text = "Please enter the path to the input files:", fg = 'slate blue', font = (FONT_TYPE, int(FONT_SIZE)))
        input.grid(row=row, column=column, padx = PADDING, pady = PADDING*2, sticky = W, columnspan = 2)
        row += 1
        
        #get node and edge file
        self.title = make_entry(self.app, "Hive Title:", width = TEXT_ENTRY_WIDTH, row = row, column = column, bg = 'aliceblue')
        row +=1
        self.nodes = make_entry(self.app, "Nodes:", width = TEXT_ENTRY_WIDTH, row = row, column = column, bg = 'aliceblue')
        column += 2
        self.bnodes = Button(self.app, text="Browse", command=self.load_node_file, width=MENU_WIDTH)
        self.bnodes.grid(row=row, column=column, sticky=W)        
        
        column = 0
        row += 1 
        self.edges = make_entry(self.app, "Edges:", width = TEXT_ENTRY_WIDTH, row = row, column = column, bg = 'aliceblue')
        column += 2
        self.bedges = Button(self.app, text="Browse", command=self.load_edge_file, width=MENU_WIDTH)
        self.bedges.grid(row=row, column=column, sticky=W)       
        
        #for debugging/development purposes
        self.title.insert(0,"hive1")
        self.nodes.insert(0,NODES)
        self.edges.insert(0,EDGES)
        
        column -=1
        row += 1
        #add button to update parameters data
        bSubmit = Button(self.app)
        bSubmit.grid(row=row, column=column, padx = PADDING, pady = PADDING*2, columnspan = 4)
        bSubmit.configure(text = "Submit network", width=30, command=self.update, fg = 'blue', font = (FONT_TYPE, int(FONT_SIZE)))
        
        self.app2 = Frame(self)
        row = 0
        column = 0
        self.app2.grid()
        
        input = Label(self.app2, text = "Enter the plotting parameters:", fg = 'slate blue', font = (FONT_TYPE, int(FONT_SIZE)))
        input.grid(row=row, column=column, padx = PADDING, pady = PADDING*2, columnspan = 2, sticky = W)
        #column += 1
        
        #make different option menus
        row += 1
        self.debugOpt, self.debugVar = make_options(self.app2, 'Debug:', row = row, column = column, selections = debugOptions)
        row += 1
        self.axesOpt, self.axesVar = make_options(self.app2, 'Number of Axes:', row = row, column = column, selections = axesOptions)
        self.axesVar.set('3')
        column += 2
        self.doubleOpt, self.doubleVar = make_options(self.app2, 'Double axes:', row = row, column = column, selections = doubleOptions)
        self.doubleVar.set('False')
        row += 1
        column = 0
        self.assignmentOpt, self.assignmentVar = make_options(self.app2, 'Node Assignment Rule:', row = row, column = column, selections = assignmentOptions)
        column += 2
        self.positionOpt, self.positionVar = make_options(self.app2, 'Node Position Rule:', row = row, column = column, selections = positionOptions)
        self.positionVar.set('clustering')
        row += 1
        column = 0
        self.edgeStyleOpt, self.edgeStyleVar = make_options(self.app2, 'Edge Style Rule:', row = row, column = column, selections = edgeStyleOptions, command = self.load_parameters)
        
        #add button to submit parameters
        column +=1
        bLoad = Button(self.app2)
        bLoad.grid(padx = 10, pady = 40, columnspan = 5)
        bLoad.configure(text = "Load parameters", width=20, command=self.load_parameters, font = (FONT_TYPE, int(0.9*FONT_SIZE)))

        
        #add button to close window
        self.bClose = Button(self)
        #self.bClose.grid(padx = PADDING*2, pady = PADDING*2, columnspan = 4, sticky = E)
        self.bClose.configure(text = "Close window", width=10, command=self.close_window, font = (FONT_TYPE, int(0.8*FONT_SIZE)))

        self.load_parameters()

    def reset_option_menu(self, w, variable, options, index=None, caption = None):
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

    def test(self):
        print 'woohoo'
        
    def load_node_file(self):
        fname = tkFileDialog.askopenfilename(filetypes = (("CSV files", "*.csv")
                                                     ,("Tab delimited files", "*.txt") ))
        if fname:
            self.nodes.delete(0, "end")
            self.nodes.insert(0,fname)
            return

    def load_edge_file(self):
        fname = tkFileDialog.askopenfilename(filetypes = (("CSV files", "*.csv")
                                                     ,("Tab delimited files", "*.txt") ))
        if fname:
            self.edges.delete(0, "end")
            self.edges.insert(0,fname)
            return
         
    def load_parameters(self):
        #create some optional parameters for some styling
        self.app3 = Frame(self)
        row = 0
        column = 0
        self.app3.grid()
        
        style = self.edgeStyleVar.get()
        numColors = get_num_colors(self.edges, style)
        
        if not self.loaded:
            input = Label(self.app3, text = "Change the node and edge coloring:", fg = 'slate blue', font = (FONT_TYPE, int(FONT_SIZE)))
            input.grid(row=row, column=column, padx = PADDING*2, pady = PADDING, columnspan = 2, sticky = W)
            
            row += 1
            self.colorOpt, self.colorVar = make_options(self.app3, 'Number of colors to draw edges:', row = row, column = column, selections = numColors)
            
            column += 2
            self.nodeColorOpt, self.nodeColorVar = make_options(self.app3, 'Node Color:', row = row, column = column, selections = colorOptions)
            
            row += 1
            column = 0
            self.paletteOpt, self.paletteVar = make_options(self.app3, 'Hue of color palette:', row = row, column = column, selections = colorOptions)
            
            #add button to create hive
            bCreate = Button(self.app3)
            bCreate.grid(padx = PADDING*2, pady = PADDING*2, columnspan = 4)
            bCreate.configure(text = "Create and open Hive", width=60, command=self.callback, bg = 'aliceblue', font = (FONT_TYPE, int(1.2*FONT_SIZE)))
            
            row+=1
            self.bClose.grid(padx = PADDING*2, pady = PADDING*2, columnspan = 4, sticky = E)
            
        self.loaded = True
        
        self.colorVar = self.reset_option_menu(self.colorOpt, self.colorVar, numColors)

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
        edgeStyle = self.edgeStyleVar.get()
        nodeColor = self.nodeColorVar.get()
        paletteHue = self.paletteVar.get()
        numColors = self.colorVar.get()
        
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
        
        palette = get_palette(paletteHue,int(numColors))
        
        hive = Hive(debug = debug, 
                    numAxes = axes,
                    doubleAxes = double, 
                    axisAssignRule = assignment, 
                    axisPositRule = position,
                    edgePalette = palette, 
                    edgeStyleRule = edgeStyle,
                    nodeColor = nodeColor
                    )
        hive.make_hive(nodefile, edgefile)
        url = make_html(hiveTitle, hive)
        
        webbrowser.open("file://"+url, new=2)

    def close_window(self):
        print 'Closing window...'
        self.destroy()

if __name__ == "__main__":
    app = HiveGui()
    app.mainloop()

