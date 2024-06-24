from uuid import uuid4

class Item(object):
    def __init__(self, uuid : str = "", name = "", quantity = 0, cost = 0, weight = 0, units = "each", datasheet = ""):
        super().__init__()
        if uuid == "":
            self.uuid = str(uuid4())
        else:
            self.uuid = uuid
        self.name = name
        self.quantity = quantity
        self.cost = cost
        self.weight = weight
        self.units = units
        self.datasheet = datasheet

    def printCost(self) -> str:
        return f"${self.cost*100:,:.2f}/{self.units}"
    
    def printName(self) -> str:
        return self.name.capitalize()
    
    def printQuantity(self) -> str:
        return f"{self.quantity} {self.units}"