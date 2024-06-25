import os
from sys import maxsize
from json import load
from pytest import warns
from numpy.random import randint
from uuid import uuid4
from Connection import Connection
from Item import Item

# global nameslist
# global unitslist
global conn
# global items

if ('test_inventory.sqlite') in os.listdir():
    os.remove('test_inventory.sqlite')

with open("formatted_nouns.txt", mode = "r") as fp:
    nameslist = load(fp)

test_path = os.getcwd() + '/test_inventory.sqlite'

unitslist = ["meter", "gram", "yard", "mile", "kilogram", "foot", "second", "inch", "millimeter", "ohm", "farad", "volt", "amp", "each"]

def itemFactory(uuid = "") -> Item:
    idx1 = randint(len(nameslist))
    idx2 = randint(len(nameslist))

    name = nameslist[idx1] + " " + nameslist[idx2]
    quantity = randint(maxsize)
    cost = randint(maxsize)
    weight = randint(maxsize)
    units = unitslist[randint(len(unitslist))]

    if uuid == "":
        return Item(name = name, quantity = quantity, cost = cost, weight = weight, units = units)
    else:
        return Item(uuid = uuid, name = name, quantity = quantity, cost = cost, weight = weight, units = units) 

items = [itemFactory(str(uuid4())) for i in range(1000)]

def test_init_db():
    # test that a warning is raised when connecting to a db file not in the cwd.
    global conn
    with warns(UserWarning, match = "A SQLite DB named test_inventory.sqlite was not found"):
        conn = Connection(test_path)


def test_init_item():
    # initialize a bunch of items with empty uuids and test their properties
    # this is really testing itemFactory() as much as anything
    ids = []
    for i in range(1000):
        testItem = itemFactory()
        assert len(testItem.uuid) == len(str(uuid4()))
        assert testItem.quantity >= 0
        assert testItem.cost >= 0
        assert testItem.weight >= 0
        assert testItem.units in unitslist
        ids.append(testItem.uuid)
    assert len(set(ids)) == len(ids)

def test_create_item():
    res = []
    for k in range(len(items)):
        res.append(conn.create(items[k]))
    # check that all creations worked
    assert all([i == 0 for i in res])

def test_item_from_db():
    # I initialized a bunch of items earlier and this gets them and checks if they are real
    for j in range(1000):
        testItem = conn.getItem(items[j].uuid)
        assert len(testItem.uuid) == len(str(uuid4()))
        assert testItem.quantity >= 0
        assert testItem.cost >= 0
        assert testItem.weight >= 0
        assert testItem.units in unitslist

def test_increment():
    # test increasing quantity of item

    pass

def test_decrement():
    # test decreasing quantity of item
    pass

def test_delete_item():
    # test deleting item from database
    pass
