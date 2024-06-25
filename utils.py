from numpy.random import randint
from sys import maxsize
from json import load
from Item import Item

with open("formatted_nouns.txt", mode = "r") as fp:
    nameslist = load(fp)

unitslist = ["meter", "gram", "yard", "mile", "kilogram", "foot", "second", "inch", "millimeter", "ohm", "farad", "volt", "amp", "each"]

def itemFactory(uuid = "", name = "") -> Item:
    idx1 = randint(len(nameslist))
    idx2 = randint(len(nameslist))

    if name == "":
        item_name = nameslist[idx1] + " " + nameslist[idx2]
    else:
        item_name = name
    quantity = randint(maxsize/2)
    cost = randint(maxsize)
    weight = randint(maxsize)
    units = unitslist[randint(len(unitslist))]

    if uuid == "":
        return Item(name = item_name, quantity = quantity, cost = cost, weight = weight, units = units)
    else:
        return Item(uuid = uuid, name = item_name, quantity = quantity, cost = cost, weight = weight, units = units) 
