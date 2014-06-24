'''
created  18/06/2014

by sperez

Template for GUI
'''

import sys
import os
from Tkinter import *

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
    print nodes.get()
    print edges.get()
    
def makeentry(parent, caption, width=None, **options):
    Label(parent, text=caption).pack(side=LEFT)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.pack()
    return entry

#add a label
app = Frame(root)
app.pack()
welcome = Label(app, text = "Welcome to Hive Maker!")
welcome.pack()

#add button to submit data
b = Button(root)
b.pack()
b.configure(text = "Submit", width=20, command=callback)

#get node and edge file
nodes = makeentry(app, "Nodes:", 60)
edges = makeentry(app, "Edges:", 60)

nodes.get()
edges.get()



print nodes



root.mainloop()

