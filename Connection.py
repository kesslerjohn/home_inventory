from Item import Item
import sqlite3
from sqlite3 import Error
import warnings
import os
from datetime import datetime, timezone, timedelta

class Connection(object):
    def __init__(self, dir_path, db_name):
        super().__init__()
        self.path = f"{dir_path}/{db_name}"
        self.table_init = """
        CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        quantity INTEGER,
        cost_per_unit INTEGER,
        weight FLOAT(6, 2),
        units TEXT,
        datasheet TEXT, 
        date_added TEXT
        );
        """
        if (db_name) not in os.listdir(dir_path):
            with sqlite3.connect(self.path) as conn:
                conn.cursor().execute(self.table_init)
            warnings.warn(f"A SQLite DB named {db_name} was not found at the path given. \nA new SQLite DB will be created in {dir_path}.",
                          UserWarning)
    
    # all these functions return 0 or 1 status code
    def incrementQuantity(self, item : Item, by = 1) -> int:
        if by <= 0:
            warnings.warn("You cannot increment by a non-positive value. Please use decrementQuantity to reduce the count.", UserWarning)
            return 1
        item.quantity = item.quantity + by 
        query = f'UPDATE items SET quantity = {item.quantity} WHERE uuid = "{item.uuid}"'
        with sqlite3.connect(self.path) as conn:
            conn.execute(query)
        return 0

    def decrementQuantity(self, item : Item, by = 1) -> int:
        if by > item.quantity:
            msg = """
            The quantity you are trying to remove is greater than the quantity in inventory.
            If you are sure this is the correct quantity to remove, then inventory may need to 
            be updated to reflect the correct quantity.
            """
            warnings.warn(msg, UserWarning)
            return 1
        elif by <= 0:
            warnings.warn("You cannot decrement by a non-positive value. Please use incrementQuantity to increase the count.", UserWarning)
            return 1
        item.quantity = item.quantity - by 
        query = f'UPDATE items SET quantity = {item.quantity} WHERE uuid = "{item.uuid}";'
        with sqlite3.connect(self.path) as conn:
            conn.execute(query)
        return 0

    def create(self, item : Item, path = None) -> int:
        query = """
        INSERT INTO items (uuid, name, quantity, cost_per_unit, weight, units, datasheet, date_added) 
        VALUES ("{}", "{}", {}, {}, {}, "{}", "{}", "{}");
        """.format(item.uuid, item.name, item.quantity, item.cost, item.weight, item.units, item.datasheet, item.printDateAdded)
        if path is None:
            path = os.getcwd()
        item.makeQrCode(path)
        with sqlite3.connect(self.path) as conn:
            conn.cursor().execute(query)
        return 0

    def destroy(self, item : Item) -> int:
        # remove an item from the database completely
        # may not be strictly part of the MVP, since the necessary use case is unclear
        # requires an Item and not just a uuid to enforce that the item
        # should be in the DB to begin with
        if self.getItem(item.uuid) == 1:
            return 1
        query = f'DELETE FROM items WHERE uuid="{item.uuid}";'
        with sqlite3.connect(self.path) as conn:
            conn.cursor().execute(query)
        return 0
    
    def search(self, term : str) -> list[tuple]:
        if term == "":
            return []
        query = f"SELECT * FROM items WHERE name LIKE '%{term}%';"
        with sqlite3.connect(self.path) as conn:
            res = conn.cursor().execute(query).fetchall()
        return res

    def getItem(self, uuid: str) -> Item:
        query = f'SELECT * FROM items WHERE uuid = "{uuid}";'
        with sqlite3.connect(self.path) as conn:
            res = conn.cursor().execute(query).fetchone()
        if res is None:
            warnings.warn("No item with this UUID was found in the database.", UserWarning)
            return 1
        item = Item(uuid = res[1], name = res[2], quantity = res[3], cost = res[4], weight = res[5])
        return item

    def execute_query(self, query):
        with sqlite3.connect(self.path) as conn:
            conn.cursor().execute(query)