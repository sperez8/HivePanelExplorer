'''
created  20/06/2014

by sperez

all the functions we need in the gui
to make labels, option menus, etc...
'''

from Tkinter import *

    
def make_entry(parent, caption, width=None, fill=False, side = None, **options):
    Label(parent, text=caption).pack()#side=LEFT)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    if fill:
        entry.pack(fill=X)
    elif side == 'left':
        entry.pack(side=LEFT)
    else:
        entry.pack()
    return entry

def make_options(parent, caption, options):
    Label(parent, text=caption).pack(side=LEFT)
    var = StringVar(parent)
    var.set(options[0]) #default value
    w = apply(OptionMenu, (parent, var) + tuple(options))
    w.pack(side=LEFT)
    return var