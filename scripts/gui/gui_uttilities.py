'''
created  20/06/2014

by sperez

all the functions we need in the gui
to make labels, option menus, etc...
'''

from Tkinter import *

fontType = 'Helvetica'
fontSize = 16

    
def make_entry(parent, caption, width=None, row = 0, column = 0, **options):
    Label(parent, text=caption, font = (fontType, int(fontSize))).grid(row=row, column=column, sticky = E, ipadx = 20)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.grid(row=row, column=column+1, padx = 15)
    return entry

def make_options(parent, caption, row = 0, column = 0, selections = [], **options):
    Label(parent, text=caption, font = (fontType, int(fontSize*0.9))).grid(row=row, column=column)
    var = StringVar(parent)
    var.set(selections[0]) #default value
    w = apply(OptionMenu, (parent, var) + tuple(selections))
    w.grid(row=row, column=column+1, sticky=W, padx = 5)
    return w,var

# def reset_option_menu(self, w, var, options, index=None):
#     '''reset the values in the option menu
#     
#     if index is given, set the value of the menu to
#     the option at the given index
#     '''
#     menu = w["menu"]
#     menu.delete(0, "end")
#     for string in options:
#         menu.add_command(label=string, command=lambda value=string: var(value))
#     if index is not None:
#         var.set(options[index])
#     
#     return var
