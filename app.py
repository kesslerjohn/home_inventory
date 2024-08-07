import tkinter as tk
from tkinter import ttk
from Connection import Connection
from Item import Item
from database_utils import *
import os

WARNING_SIZE = "300x100"

class App(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        container = tk.Frame(self)
        container.grid()

        self.conn = Connection(os.getcwd(), "gui_db.sqlite")

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}  
        self.titles = {MainPage: "🧰 Inventory 🧰",
                       Create: "🌼 Create 🌼",
                       Update: "🧩 Update 🧩",
                       View: "📒 Item info 📒",
                       Delete: "❌ Delete ❌",
                       ItemDisplay: "📒 Item info 📒"}
        for F in (MainPage, Create, Update, View, Delete, ItemDisplay):
  
            frame = F(container, self)
            self.frames[F] = frame 
  
            frame.grid(row = 0, column = 0, sticky = "nsew")

        self.geometry("500x300")
        self.show_frame(MainPage)
    
    def show_frame(self, f):
        frame = self.frames[f]
        self.title(self.titles[f])
        frame.tkraise()

    def show_warning(self, message):
        win = tk.Toplevel()
        win.geometry(WARNING_SIZE)
        win.title("⛔️ Warning ⛔️")
        warn = ttk.Label(win, text = message)
        warn.grid(padx=50, pady=40)
        return 1

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
        self.conn = root.conn
        self.root = root

        input_window = tk.Frame(self)
        input_window.grid(row = 1, column = 1, padx = 120, pady = 50)

        name_label = ttk.Label(input_window, text = "Name:", font = ("Roboto", 12))
        name_label.grid(row = 0, column = 0)

        name = tk.StringVar()
        name_entry = ttk.Entry(input_window, textvariable = name)
        name_entry.grid(row = 0, column = 1, columnspan=3)

        qty_label = ttk.Label(input_window, text = "Quantity: ", font = ("Roboto", 12))
        qty_label.grid(row = 1, column = 0)
        qty = tk.StringVar()
        qty_entry = ttk.Entry(input_window, textvariable = qty)
        qty_entry.grid(row = 1, column = 1, columnspan=3)

        cost_label = ttk.Label(input_window, text = "Cost: ", font = ("Roboto", 12))
        cost_label.grid(row = 2, column = 0)
        cost = tk.StringVar()
        cost_entry = ttk.Entry(input_window, textvariable = cost, width = 9)
        cost_entry.grid(row = 2, column = 1, columnspan=1)

        units_label = ttk.Label(input_window, text = "Units: ", font = ("Roboto", 12))
        units_label.grid(row = 2, column = 2)
        units = tk.StringVar()
        units_entry = ttk.Entry(input_window, textvariable = units, width = 4)
        units_entry.grid(row = 2, column = 3)

        datasheet_label = ttk.Label(input_window, text = "Datasheet: ", font = ("Roboto", 12))
        datasheet_label.grid(row = 3, column = 0)
        datasheet = tk.StringVar()
        datasheet_entry = ttk.Entry(input_window, textvariable = datasheet)
        datasheet_entry.grid(row = 3, column = 1, columnspan=3)       

        create_button = ttk.Button(input_window, text = "Create",
                                   command = lambda: self.submitQuery(name, qty, cost, units, datasheet))
        create_button.grid(row = 4, column = 1)

        main_button = ttk.Button(input_window, text = "Main Page",
                            command = lambda : root.show_frame(MainPage))
     
        main_button.grid(row = 4, column = 2, columnspan=2)

        name_entry.focus()
    
    def submitQuery(self, name, qty, cost, units, datasheet):
        if name.get() == "":
            return self.root.show_warning("You must give the item a name.")
        self.conn.create(Item(name = name.get(), quantity = qty.get(), cost = cost.get(), units = units.get(), datasheet = datasheet.get()))
        
        for sv in [name, qty, cost, units, datasheet]:
            sv.set("")

class Update(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)

        self.root = root
        self.conn = root.conn

        box = tk.Frame(self)
        box.grid(row=0, column=0, padx=150, pady=50)

        label = ttk.Label(box, text = "Scan item QR:", font = ("Roboto", 12))
        label.grid(row = 0, column = 0, columnspan = 2)

        qr = tk.StringVar()
        code_entry = ttk.Entry(box, textvariable = qr)
        code_entry.grid(row = 1, column = 0, columnspan = 2)

        get_button = ttk.Button(box, text = "Get item", command = lambda: self.get_response(qr))
        get_button.grid(row = 2, column = 0)
    
        main_button = ttk.Button(box, text="Main Page",
                            command = lambda : self.root.show_frame(MainPage))
        main_button.grid(row = 2, column = 1)

        code_entry.focus()

    def get_response(self, qr):
        item = self.conn.getItem(qr.get())
        qr.set("")
        if item == 1:
            return self.root.show_warning("No item with this UUID was found.")
        
        
class View(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        
        self.conn = root.conn
        self.root = root

        label = ttk.Label(self, text = "Scan item QR:", font = ("Roboto", 12))
        label.grid(row = 0, column = 0, columnspan = 2)

        qr = tk.StringVar()
        code_entry = ttk.Entry(self, textvariable = qr)
        code_entry.grid(row = 1, column = 0, columnspan = 2)

        get_button = ttk.Button(self, text = "Get item", command = lambda: self.get_response(qr))
        get_button.grid(row = 2, column = 0)
    
        main_button = ttk.Button(self, text="Main Page",
                            command = lambda : root.show_frame(MainPage))
        main_button.grid(row = 2, column = 1)

        code_entry.focus()

    def get_response(self, qr):
        item = self.conn.getItem(qr.get())
        qr.set("")
        if item == 1:
            win = tk.Toplevel()
            win.geometry(WARNING_SIZE)
            warn = ttk.Label("")
            self.root.show_frame(MainPage)
            return 1
        self.root.frames[ItemDisplay].setItem(item = item)
        self.root.show_frame(ItemDisplay)
            
class Delete(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text = "Delete", font = ("Roboto", 35))
        label.grid()

        main_button = ttk.Button(self, text="Main Page",
                            command = lambda : root.show_frame(MainPage))
        
        main_button.grid(row = 1, column = 1, padx = 10, pady = 10)

class ItemDisplay(tk.Frame):
    def __init__(self, parent, root):
        tk.Frame.__init__(self, parent)
        name_label = ttk.Label(self, text = "Name: ", font = ("Roboto", 12))
        name_label.grid(row = 0, column = 0)

        qty_label = ttk.Label(self, text = "Quantity: ", font = ("Roboto", 12))
        qty_label.grid(row = 1, column = 0)

        cost_label = ttk.Label(self, text = "Cost: ", font = ("Roboto", 12))
        cost_label.grid(row = 2, column = 0)

        main_button = ttk.Button(self, text="Main Page",
                            command = lambda : root.show_frame(MainPage))
        
        main_button.grid(row = 3, column = 1, padx = 10, pady = 10)

    def setItem(self, item : Item): 
        i_name_label = ttk.Label(self, text = item.printName(), font = ("Roboto", 12))
        i_name_label.grid(row = 0, column = 1)

        i_qty_label = ttk.Label(self, text = item.printQuantity(), font = ("Roboto", 12))
        i_qty_label.grid(row = 1, column = 1)

        i_cost_label = ttk.Label(self, text = item.printCost(), font = ("Roboto", 12))
        i_cost_label.grid(row = 2, column = 1)

app = App()
app.mainloop()