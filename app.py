import tkinter as tk
from tkinter import ttk
from Connection import Connection
from Item import Item
from database_utils import *
from math import floor

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
                       Update: "🧩 Update 🧩",
                       View: "📒 Item info 📒",
                       Delete: "❌ Delete ❌"}
        # iterating through a tuple consisting
        # of the different page layouts
        for F in (MainPage, Create, Update, View, Delete):
  
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

        delete_button = tk.Button(inner_frame, text="Delete", 
                                   command = lambda : root.show_frame(Delete), width = 20, height = 5)

        create_button.grid(row = 0, column = 0)
        update_button.grid(row = 0, column = 1)
        view_button.grid(row = 1, column = 0)
        delete_button.grid(row = 1, column = 1)
  
class Create(tk.Frame):
    def __init__(self, parent, root):
        
        tk.Frame.__init__(self, parent)

        input_window = tk.Frame(self)
        input_window.grid(row = 1, column = 1, padx = 120, pady = 50)

        features = ["Item name", "Units", "Cost per unit", "Quantity", "Datasheet"]

        name_label = ttk.Label(input_window, text = "Name:", font = ("Roboto", 12))
        name_label.grid(row = 0, column = 0)

        self.name = tk.StringVar()
        name_entry = ttk.Entry(input_window, textvariable=self.name)
        name_entry.grid(row = 0, column = 1, columnspan=3)

        self.qty = tk.StringVar()
        qty_entry = ttk.Entry(input_window, textvariable=self.qty)
        qty_entry.grid(row = 1, column = 1, columnspan=3)

        self.cost = tk.StringVar()
        cost_entry = ttk.Entry(input_window, textvariable=self.cost, width = 14)
        cost_entry.grid(row = 2, column = 1, columnspan=2)

        self.units = tk.StringVar()
        units_entry = ttk.Entry(input_window, textvariable=self.units, width = 4)
        units_entry.grid(row = 2, column = 3)

        self.datasheet = tk.StringVar()
        datasheet_entry = ttk.Entry(input_window, textvariable=self.datasheet)
        datasheet_entry.grid(row = 3, column = 1, columnspan=3)       

        create_button = ttk.Button(input_window, text = "Create",
                                   command = lambda: self.submitQuery())
        create_button.grid(row = 4, column = 1)

        # button to show frame 2 with text
        # layout2
        main_button = ttk.Button(input_window, text = "Main Page",
                            command = lambda : root.show_frame(MainPage))
     
        # putting the button in its place 
        # by using grid
        main_button.grid(row = 4, column = 2, columnspan=2)

        name_entry.focus()
    
    def submitQuery(self):
        print(f"""Created item:
            Name: {self.name.get()}
            Quantity: {self.qty.get()} {self.units.get()}
            Cost: {self.cost.get()} / {self.units.get()}
            Datasheet at: {self.datasheet.get()}
              """)
        
        for sv in [self.name, self.qty, self.units, self.cost, self.datasheet]:
            sv.set("")


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
        
        main_button.grid(row = 1, column = 1, padx = 10, pady = 10)

class Delete(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Delete", font = ("Roboto", 35))
        label.grid()

        main_button = ttk.Button(self, text="Main Page",
                            command = lambda : root.show_frame(MainPage))
        
        main_button.grid(row = 1, column = 1, padx = 10, pady = 10)


app = App()
app.mainloop()