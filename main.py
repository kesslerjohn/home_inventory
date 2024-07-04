import os
import warnings
from database_utils import *
from Item import Item
from Connection import Connection

# basic idea:
# generate QR codes for inventory
# interface with the raspberry pi or an old
# salvaged computer that I can just run all the time

# need functionality to generate QR data when I want
# and update inventory database by adding/removing components
# this will work for salvaged electronics
# and garden supplies. 

# want to store datasheets for some items
# as a file path. 
# should I keep a category column?

# starting with sqlite3 for MVP and will deploy to
# network SQL server later

# | uuid | name | quantity | cost | weight | units | datasheet | date_added |
# |------|------|----------|------|--------|-------|-----------|------------|
#                                   ...

# unique and constant, should be available everywhere
# connection stores the connection to the sql database
# mode is an enumerable of operating modes:
# 1. 'modify item' is the default mode. Here, the user
#       can scan an existing barcode, and then choose
#       to either add or remove a number of items 
#       of that type.
# 2. 'reset' prepares to completely remake the 
#       inventory, item by item. 
# 3. 'create_item' 
global conn
global mode
global modes
modes = ['reset', 'create_item', 'modify_item', 'delete_item']
modes_d = {
    'reset': 0,
    'create_item': 0,
    'modify_item': 0,
    'delete_item': 0
}
mode = 'modify_item'

#TODO: Refactor all this to handle new data structures.

def setup():
    path = os.getcwd() + '/test_inventory.sqlite'
    conn = Connection(path)

    return 0

def loop():
    userEvent = input(":> ")
    if userEvent not in modes:
            print("Please give a valid mode")
    else:
        mode = userEvent
    
    if mode == 'modify_item':
        return 0
    elif mode == "create_item":
        name = input("Item name: ")
        quantity = input("Quantity: ")
        cost = input("Cost: ")
        weight = input("Weight: ")
        units = input("Units: ")
        datasheet = input("Datasheet: ")
        item = Item(name = name, quantity = int(quantity), cost = int(cost), weight = float(weight), units = units, datasheet = datasheet)
        conn.create(item)
        qr = bool(int(input("Item added to database. Make QR Code? ")))
        if qr:
            item.makeQrCode(os.getcwd())
        mode = "start"
    return 0

if __name__ == "__main__":
    setup()

    while True:
        loop()