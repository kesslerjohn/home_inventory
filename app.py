import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
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

class App(ctk.CTk):

    def __init__(self, *args, **kwargs):
        ctk.CTk.__init__(self, *args, **kwargs)
        ctk.set_appearance_mode("system")
        ctk.set_default_color_theme("green")
        container = ctk.CTkFrame(self)
        container.pack(padx = 60, pady = 20, fill="both", expand = True)

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

class MainPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        ctk.CTkFrame.__init__(self, parent)

        label = ctk.CTkLabel(self, text = "QR Inventory", font = ("Roboto", 35))
        label.grid(row = 0, column = 4, padx = 10, pady = 10)

        button1 = ctk.CTkButton(self, text ="Create",
        command = lambda : controller.show_frame(Create))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
class Create(ctk.CTkFrame):
    def __init__(self, parent, controller):
        
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text ="Create", font = ("Roboto", 35))
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        self.features = ["Item name", "Units", "Cost per unit", "Quantity", "Weight", "Datasheet"]

        for i in range(len(self.features)):
            info = ctk.CTkEntry(placeholder_text=self.features[i], master=parent)
            info.grid(row=i, column = 0, padx = 10, pady = 10)

        # button to show frame 2 with text
        # layout2
        main_button = ctk.CTkButton(self, text ="Main Page",
                            command = lambda : controller.show_frame(MainPage))
     
        # putting the button in its place 
        # by using grid
        main_button.grid(row = 6, column = 1, padx = 10, pady = 10)
        

app = App()
app.mainloop()