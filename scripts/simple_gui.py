'''
created  18/06/2014

by sperez

Template for GUI
'''

from Tkinter import *

#create window
root  = Tk()
root.title("Hive Plot Maker")
root.geometry("300x200")

#add a label
app = Frame(root)
app.grid()
label = Label(app, text = "Welcome to Hive Maker!")
label.grid()

#add butons
buttonNodes = Button(app)
buttonEdges = Button(app)
buttonNodes.grid()
buttonEdges.grid()
buttonNodes.configure(text = "Nodes")
buttonEdges.configure(text = "Edges")



root.mainloop()
