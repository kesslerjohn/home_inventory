from Item import Item
import sqlite3
from sqlite3 import Error
import warnings
import os

class Connection(object):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.table_init = """
        CREATE TABLE IF NOT EXISTS items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        uuid TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        quantity INTEGER,
        cost_per_unit INTEGER,
        weight FLOAT(6, 2),
        units TEXT,
        datasheet TEXT
        );
        """
        if (path.split("/")[-1]) not in os.listdir():
            with sqlite3.connect(path) as conn:
                conn.cursor().execute(self.table_init)
            warnings.warn(f"A SQLite DB named {path.split('/')[-1]} was not found at the path given. A new SQLite DB will be created.",
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

    def create(self, item : Item) -> int:
        query = """
        INSERT INTO items (uuid, name, quantity, cost_per_unit, weight, units, datasheet) 
        VALUES ("{}", "{}", {}, {}, {}, "{}", "{}");
        """.format(item.uuid, item.name, item.quantity, item.cost, item.weight, item.units, item.datasheet)
        with sqlite3.connect(self.path) as conn:
            conn.cursor().execute(query)
        return 0

    def destroy(self, item : Item) -> int:
        return 0
    
    def search(self, term : str) -> list[tuple]:
        query = f"SELECT * FROM items WHERE name LIKE '%{term}%';"
        with sqlite3.connect(self.path) as conn:
            res = conn.cursor().execute(query).fetchall()
        return res

    def getItem(self, uuid: str) -> Item:
        query = f'SELECT * FROM items WHERE uuid = "{uuid}";'
        with sqlite3.connect(self.path) as conn:
            res = conn.cursor().execute(query).fetchone()
        item = Item(uuid = res[1], name = res[2], quantity = res[3], cost = res[4], weight = res[5])
        return item

    def execute_query(self, query):
        with sqlite3.connect(self.path) as conn:
            conn.cursor().execute(query)