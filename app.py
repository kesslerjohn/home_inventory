import tkinter as tk
from tkinter import ttk
from Connection import Connection
from Item import Item
from database_utils import *

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.grid()

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  
        self.titles = {MainPage: "🧰 Inventory 🧰",
                       Create: "🌼 Create 🌼",
                       Update: "🧩 Modify 🧩",
                       View: "📒 Item info 📒"}
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (MainPage, Create, Update, View):
  
            frame = F(container, self)
  
            # initializing frame of that object from
            # startpage, page1, page2 respectively with 
            # for loop
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.geometry("500x300")
        self.show_frame(MainPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        self.title(self.titles[cont])
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        inner_frame = tk.Frame(self)
        inner_frame.grid(row = 0, column = 0, padx = 25, pady = 25, sticky = "nsew")
        inner_frame.grid_rowconfigure(0, weight=1)
        inner_frame.grid_rowconfigure(1, weight=1)

        inner_frame.grid_columnconfigure(0, weight = 0)
        inner_frame.grid_columnconfigure(1, weight = 0)

        create_button = tk.Button(inner_frame, text ="Create",
                                   command = lambda : root.show_frame(Create), width = 20, height = 10)

        update_button = tk.Button(inner_frame, text ="Update",
                                   command = lambda : root.show_frame(Update), width = 20, height = 10)

        view_button = tk.Button(inner_frame, text="View", 
                                   command = lambda : root.show_frame(View), width = 20, height = 5)
     
        # putting the button in its place by
        # using grid
        create_button.grid(row = 0, column = 0)
        update_button.grid(row = 0, column = 1)
        view_button.grid(row = 1, column = 0)

  
class Create(tk.Frame):
    def __init__(self, parent, root):
        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text ="Create", font = ("Roboto", 35))
        label.grid(row = 0, column = 6, padx = 10, pady = 10)

        input_window = tk.Frame(self)
        input_window.rowconfigure(5)
        input_window.columnconfigure(3)
        input_window.grid(padx = 10, pady = 10)
  
        features = ["Item name", "Units", "Cost per unit", "Quantity", "Datasheet"]

        # TODO: These should all span both columns except for cost and units
        name_entry = ttk.Entry(input_window)
        name_entry.grid(row = 0, column = 1, columnspan=3)

        name_label = ttk.Label(input_window, text = "Name:", font = ("Roboto", 12))
        name_label.grid(row = 0, column = 1)

        qty_entry = ttk.Entry(input_window)
        qty_entry.grid(row = 1, column = 1, columnspan=3)

        cost_entry = ttk.Entry(input_window)
        cost_entry.grid(row = 2, column = 1, columnspan=2)

        units_entry = ttk.Entry(input_window)
        units_entry.grid(row = 2, column = 3)

        datasheet_entry = ttk.Entry(input_window)
        datasheet_entry.grid(row = 3, column = 1, columnspan=3)       

        create_button = ttk.Button(self, text = "Create",
                                   command = lambda: print("Create button pushed"))
        create_button.grid(row = 4, column = 0)

        # button to show frame 2 with text
        # layout2
        main_button = ttk.Button(self, text = "Main Page",
                            command = lambda : root.show_frame(MainPage))
     
        # putting the button in its place 
        # by using grid
        main_button.grid(row = 4, column = 1)

class Update(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        self.rowconfigure(2, weight = 1)
        self.columnconfigure(4)
        label = ttk.Label(self, text = "Scan item QR:", font = ("Roboto", 12))
        label.grid(row = 0, column = 0)
    
        main_button = ttk.Button(self, text="Main Page",
                            command = lambda : root.show_frame(MainPage))
        main_button.grid(row = 2)

class View(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "View", font = ("Roboto", 35))
        label.grid()

        main_button = ttk.Button(self, text="Main Page",
                            command = lambda : root.show_frame(MainPage))
        
        main_button.grid(row = 6, column = 1, padx = 10, pady = 10)



app = App()
app.mainloop()