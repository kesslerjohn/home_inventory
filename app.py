import tkinter as tk
from tkinter import ttk
from Connection import Connection
from Item import Item
from database_utils import *

#events_d = {
#    'reset': reset,
#    'create': create_item_tk,
#    'modify': modify_item,
#    'delete': delete_item,
#    'view': view_item_info
#}

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(padx = 10, pady = 5, fill="both", expand = True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  
  
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (MainPage, Create):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.geometry("500x300")
        self.show_frame(MainPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = tk.Label(self, text = "QR Inventory", font = ("Roboto", 35))
        label.grid(row = 0, column = 4, padx = 10, pady = 10)

        button1 = tk.Button(self, text ="Create",
        command = lambda : controller.show_frame(Create))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
class Create(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text ="Create", font = ("Roboto", 35))
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        self.features = ["Item name", "Units", "Cost per unit", "Quantity", "Weight", "Datasheet"]

        for i in range(len(self.features)):
            info = tk.Entry(master=parent)
            info.grid(row=i, column = 0, padx = 10, pady = 10)

        # button to show frame 2 with text
        # layout2
        main_button = tk.Button(self, text ="Main Page",
                            command = lambda : controller.show_frame(MainPage))
     
        # putting the button in its place 
        # by using grid
        main_button.grid(row = 6, column = 1, padx = 10, pady = 10)
        

app = App()
app.mainloop()