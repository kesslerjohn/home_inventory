import os
import warnings
from database_utils import *
from Item import Item
from Connection import Connection
from shutil import copy

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

def reset(userEvent):
    global conn
    next = True
    while next:
        print("\n"*10 + "Create next item.\n" + "="*10)
        name = input(":> Item name: ")
        quantity = input(":> Quantity: ")
        cost = input(":> Cost: ")
        weight = input(":> Weight: ")
        units = input(":> Units: ")
        datasheet = input(":> Datasheet: ")
        conn.create(Item(name = name, quantity = quantity, cost = cost, weight = weight, units = units, datasheet = datasheet))

        userEvent = input("Continue? y/n ")
        if userEvent == "n":
            next = False
        return 0

def create_item(userEvent):
    global conn
    return 0

def modify_item(userEvent):
    global conn
    uuid = input("Scan QR: ")
    item = conn.getItem(uuid)
    add = ({'a': True, 'r': False})[input("Add or remove items? a/r").lower()]
    if add:
        by = int(input("Add how many? "))
        return conn.incrementQuantity(item, by = by)
    else:
        by = int(input("Remove how many? "))
        return conn.decrementQuantity(item, by = by)

def delete_item(userEvent):
    global conn 
    return 0

events_d = {
    'reset': reset,
    'create_item': create_item,
    'modify_item': modify_item,
    'delete_item': delete_item
}
mode = 'modify_item'

#TODO: Refactor all this to handle new data structures.

def setup():
    path = os.getcwd() + '/fake_inventory.sqlite'
    return Connection(path)

def loop():
    global conn
    userEvent = input(":> ")
    if userEvent not in events_d.keys():
            print("Please give a valid mode")
    else:
        mode = events_d[userEvent]
        mode(conn)
    return 0

if __name__ == "__main__":
    conn = setup()

    while True:
        loop()