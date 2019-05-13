# -*- coding: utf-8 -*-
"""
Created on Mon Apr 15 09:27:32 2019

@author: William Keilsohn
"""

'''
General overview of Python classes. Came in handy when 
trying to remember syntax. Please consider it a general citation:
    https://docs.python.org/3/tutorial/classes.html
'''

'''
Due to the nature of graphs always being printed out of loops,
I am using a GUI to try to display them while running.
Here are my general citations for my GUI package(s):
    https://docs.python.org/3/library/tk.html#tkinter
    https://docs.python.org/3/library/tkinter.html#tkinter-modules
    https://stackoverflow.com/questions/23901168/how-do-i-insert-a-jpeg-image-into-a-python-tkinter-window
    https://www.hackerearth.com/practice/python/object-oriented-programming/classes-and-objects-i/tutorial/
    
'''

# Import needed packages:
import tkinter as tk
from PIL import ImageTk, Image

# Read related documents:
# https://docs.python.org/2.0/ref/exec.html
graphs = 'C:/Users/kingw/Desktop/Data_Science_Project/graphs.py'
exec(open(graphs).read())

import questions as qu

# Need a global variable:
size = 500

# Create classes:

class windowFrame(tk.Frame):
    
    def __init__(self, master = None):
        super().__init__(master)
        self.pack()
        self.createGraph()
        
        
    def createGraph(self): 
        # https://stackoverflow.com/questions/23224574/tkinter-create-image-function-error-pyimage1-does-not-exist
        # https://stackoverflow.com/questions/23901168/how-do-i-insert-a-jpeg-image-into-a-python-tkinter-window
        # https://www.c-sharpcorner.com/blogs/basics-for-displaying-image-in-tkinter-python ## This page was super helpful!!
        # https://stackoverflow.com/questions/38680668/tkinter-window-and-background-image-dont-align-properly
        im_path = "C:/Users/kingw/Desktop/Data_Science_Project/py_graphs/"
        #---#
        self.canvas = tk.Canvas(self.master, width = size - 50, height = size - 50)
        self.canvas.pack(side = 'top', fill = 'both', expand = 'yes')
        self.image = ImageTk.PhotoImage(Image.open(im_path + 'fig.png'))
        self.canvas.create_image(250, 260, anchor = 'center', image = self.image)
        #---#
        self.quit = tk.Button(self, text = "Quit", fg = 'blue', command = self.master.destroy)
        self.quit.pack(side = 'bottom')
    
class windowDraw:
    
    def sizeWindow(df): # Please see comment citations at top. 
        root = tk.Tk()
        win = windowFrame(root)
        lst = list(df)
        win.master.title(str(lst[1]) + ' vs ' + str(lst[0]))
        win.master.maxsize(size, size)
        win.master.minsize(size, size)        
        win.mainloop()
        
class graphLogic:
    
    def graphDisplay(df, num1, num2 = 0):
        if num1 >= 3:
            lineGrapher(df, num2)
        else:
            boxGrapher(df, num2)
            
    def askForGraph(df, num):
        in_val = input("\nWould you like a graph for your data? (Y/N): ")
        if in_val in ['Yes', 'Y', 'y', 'yes', 'YES', 'YAAASSSS', 'YeS', 'yis']:
            graphLogic.graphDisplay(df, num)
            windowDraw.sizeWindow(df)
        
    def allGraphMaker(df):
        for index, row in df.iterrows():
            lst = df.iloc[index, :]
            data = getattr(qu.dataSets, 'frameMaker')(*lst[:-1]) # https://stackoverflow.com/questions/11881700/call-function-with-a-dynamic-list-of-arguments-in-python
            graphLogic.graphDisplay(data, lst[-1], index)
            del data # Turns out the computer crashes w/o this line.
            
    def graphAsker(df):
        in_val = input('Would you like to make ALL the graphs?(Y/N): ')
        if in_val in ['Y', 'y', 'yes' ,'YES', 'yis', 'Yes', 'yEs', 'yeS']:
            graphLogic.allGraphMaker(df)
            
