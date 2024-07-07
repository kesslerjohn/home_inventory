import tkinter as tk
from tkinter import ttk
import customtkinter as ctk

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
        for F in (MainPage, Page1):
  
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

        button1 = ctk.CTkButton(self, text ="Page 1",
        command = lambda : controller.show_frame(Page1))
     
        # putting the button in its place by
        # using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)
  
# second window frame page1 
class Page1(ctk.CTkFrame):
     
    def __init__(self, parent, controller):
         
        ctk.CTkFrame.__init__(self, parent)
        label = ctk.CTkLabel(self, text ="Page 1", font = ("Roboto", 35))
        label.grid(row = 0, column = 4, padx = 10, pady = 10)
  
        # button to show frame 2 with text
        # layout2
        button1 = ctk.CTkButton(self, text ="Main Page",
                            command = lambda : controller.show_frame(MainPage))
     
        # putting the button in its place 
        # by using grid
        button1.grid(row = 1, column = 1, padx = 10, pady = 10)

app = App()
app.mainloop()