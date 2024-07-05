import os
import warnings
from database_utils import *
from Item import Item
from Connection import Connection
import customtkinter as ctk


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
global ref 

def reset(userEvent):
    setup('temp_resetdb.sqlite')
    next = True
    while next:
        create_item(userEvent)
        if input("Create another item? y/n ") == "n":
            next = False
    print("Done. ")

    return 0

def create_item(userEvent):
    print("\n"*10 + "Create an item.\n" + "="*10)
    features = ["Item name", "Units", "Cost per unit", "Quantity", "Weight", "Datasheet"]
    userIn = []
    for f in features:
        temp = input(f":> {f}: ")
        if temp.lower() == "q":
            print("Exiting. This item will not be created. ")
            return 0
        else:
            userIn.append(temp)
    conn.create(Item(name = userIn[0], units = userIn[1], cost = userIn[2], quantity = userIn[3], weight = userIn[4], datasheet = userIn[5]))
    print("Done. ")
    return 0

def modify_item(userEvent):
    uuid = input("Scan QR: ")
    item = conn.getItem(uuid)
    if item == 1:
        return 1
    if (input("Add or remove items? a/r").lower() == "a"):
        by = int(input("Add how many? "))
        return conn.incrementQuantity(item, by = by)
    else:
        by = int(input("Remove how many? "))
        return conn.decrementQuantity(item, by = by)

def delete_item(userEvent):
    uuid = input("Scan QR: ")
    item = conn.getItem(uuid) 
    return conn.destroy(item)

def view_item_info(userEvent):
    uuid = input("Scan QR: ")
    item = conn.getItem(uuid)
    if item == 1:
        return 1
    disp = """
    Item name: {}
    Quantity: {}
    Cost: {}
    Weight: {}g
    Added on: {}
    """.format(item.printName(), item.printQuantity(), item.printCost(), item.weight, item.printDateAdded())
    print(disp)

events_d = {
    'reset': reset,
    'create': create_item,
    'modify': modify_item,
    'delete': delete_item,
    'view': view_item_info
}

def setup(db_file):
    return Connection(ref, db_file)

def loop():
    global conn
    print("Enter mode: ")
    userEvent = input(":> ")
    if userEvent not in events_d.keys():
            print("Please give a valid mode")
    else:
        mode = events_d[userEvent]
        mode(conn)
    return 0

if __name__ == "__main__":
    ref = "/".join(__file__.split("/")[:-1])

    conn = setup('/test_inventory.sqlite')

    while True:
        loop()