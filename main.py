import os
import warnings
from database_utils import *
from qr_utils import *
from Item import Item
from Connection import Connection

# basic idea:
# generate QR codes for inventory
# buy a mini QR scanner to handle reading
# to avoid having to build that hardward myself
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

# | uuid | name | quantity | cost | weight | units | datasheet |
# |------|------|----------|------|--------|-------|-----------|
#                   ...

# unique and constant, should be available everywhere
# connection stores the connection to the sql database
# mode is an enumerable of operating modes:
# 1. 'start' is the general standby mode. In this mode,
#       the device waits for 
# 2. 'reset' prepares to completely remake the 
#       inventory, item by item. 
# 3. 'create_item' 
global connection
global mode
global modes
modes = ['start', 'reset', 'create_item', 'modify_item', 'delete_item']

#TODO: Refactor all this to handle new data structures.

def setup():
    path = os.getcwd() + '/test_inventory.sqlite'
    connection = Connection(path)

    return connection

def loop():
    userEvent = input(":> ")
    if mode == "start":
        if userEvent not in modes:
            print("Please give a valid mode")
        else:
            mode = userEvent
    elif mode == "create_item":
        insert, qr = newItem()
        mode = "start"
    return 0

if __name__ == "__main__":
    connection = setup()

    insert, qr = newItem()

    print("QR created.")
    qr.save("test.png")

    execute_query(connection, insert)

    while True:
        loop()