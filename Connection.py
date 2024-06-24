from Item import Item
import sqlite3
from sqlite3 import Error
import warnings

class Connection(object):
    def __init__(self, path):
        super().__init__()
        self.path = path
    
    # all these functions return 0 or 1 status code
    def incrementQuantity(self, item : Item, by = 1) -> int:
        item.quantity = item.quantity + by 
        query = f"UPDATE items SET quantity = {item.quantity} WHERE uuid = {item.uuid}"
        try:
            with sqlite3.connect(self.path) as conn:
                conn.execute(query)
            return 0
        except Error:
            raise

    def decrementQuantity(self, item : Item, by = 1) -> int:
        if by > item.quantity:
            msg = """
            The quantity you are trying to remove is greater than the quantity in inventory.
            If you are sure this is the correct quantity, then inventory may need to be updated
            to reflect the correct quantity.
            """
            warnings.warn(msg)
        item.quantity = item.quantity - by 
        query = f"UPDATE items SET quantity = {item.quantity} WHERE uuid = {item.uuid}"
        try:
            with sqlite3.connect(self.path) as conn:
                conn.execute(query)
            return 0
        except Error:
            raise

    def create(self, item : Item) -> int:
        return 0

    def destroy(self, item : Item) -> int:
        return 0
    
    def search(self, term : str) -> list[tuple]:
        query = f"SELECT * FROM items WHERE name LIKE '%{term}%';"
        try:
            with sqlite3.connect(self.path) as conn:
                res = conn.cursor().execute(query).fetchall()
            return res
        except Error:
            raise

    def getItem(self, uuid: str) -> Item:
        query = f'SELECT * FROM items WHERE uuid = "{uuid}";'
        try:
            with sqlite3.connect(self.path) as conn:
                res = conn.cursor().execute(query).fetchone()
            item = Item(uuid = res[1], name = res[2], quantity = res[3], cost = res[4], weight = res[5])
            return item
        except Error:
            raise

    def execute_query(self, query):
        try:
            with sqlite3.connect(self.path) as conn:
                conn.cursor().execute(query)
        except Error:
            raise