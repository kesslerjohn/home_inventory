import tkinter as tk
from tkinter import ttk
from Connection import Connection
from Item import Item
from database_utils import *

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.pack(padx = 10, pady = 5, fill="both", expand = True)

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
  
            frame.grid(row = 0, column = 0, sticky ="nsew")

        self.geometry("500x300")
        self.show_frame(MainPage)
    
    def show_frame(self, cont):
        frame = self.frames[cont]
        self.title(self.titles[cont])
        frame.tkraise()

class MainPage(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        self.rowconfigure(2, weight=2)
        self.columnconfigure(2, weight=1)

        #label = ttk.Label(self, text = "QR Inventory", font = ("Roboto", 35))
        #label.grid(row = 0, column = 0, padx = 10, pady = 10)

        create_button = ttk.Button(self, text ="Create",
                                   command = lambda : root.show_frame(Create))

        update_button = ttk.Button(self, text ="Update",
                                   command = lambda : root.show_frame(Update))

        view_button = ttk.Button(self, text="View", 
                                   command = lambda : root.show_frame(View))
     
        # putting the button in its place by
        # using grid
        create_button.grid(row = 0, column = 0, padx = 10, pady = 10)
        update_button.grid(row = 0, column = 1, padx = 10, pady = 10)
        view_button.grid(row = 1, column = 0, padx = 10, pady = 10)

  
class Create(tk.Frame):
    def __init__(self, parent, controller):
        
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text ="Create", font = ("Roboto", 35))
        label.grid(row = 0, column = 6, padx = 10, pady = 10)
  
        self.features = ["Item name", "Units", "Cost per unit", "Quantity", "Weight", "Datasheet"]

        for i in range(len(self.features)):
            info = ttk.Entry(master=parent)
            info.grid(column=0)

        # button to show frame 2 with text
        # layout2
        main_button = ttk.Button(self, text ="Main Page",
                            command = lambda : controller.show_frame(MainPage))
     
        # putting the button in its place 
        # by using grid
        main_button.grid(row = 6, column = 1, padx = 10, pady = 10)

class Update(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text ="Scan item QR", font = ("Roboto", 35))
        label.grid(row = 0, column = 4, padx = 10, pady = 10)

        entrybox = ttk.Entry(master=parent)
        entrybox.grid()
    
        main_button = ttk.Button(self, text="Main Page",
                            command = lambda : root.show_frame(MainPage))
        
        main_button.grid(row = 6, column = 1, padx = 10, pady = 10)

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