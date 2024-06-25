from os import remove, listdir, getcwd
from sys import maxsize
from json import load
from pytest import warns
from numpy.random import randint
from uuid import uuid4
from Connection import Connection
from Item import Item
import pytest

global conn
global indexItem
indexItem = 0

with open("formatted_nouns.txt", mode = "r") as fp:
    nameslist = load(fp)

test_path = getcwd() + '/test_inventory.sqlite'

unitslist = ["meter", "gram", "yard", "mile", "kilogram", "foot", "second", "inch", "millimeter", "ohm", "farad", "volt", "amp", "each"]

def itemFactory(uuid = "") -> Item:
    idx1 = randint(len(nameslist))
    idx2 = randint(len(nameslist))

    name = nameslist[idx1] + " " + nameslist[idx2]
    quantity = randint(maxsize/2)
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
    if ('test_inventory.sqlite') in listdir():
        remove('test_inventory.sqlite')

    global conn
    with warns(UserWarning, match = "A SQLite DB named test_inventory.sqlite was not found"):
        conn = Connection(test_path)

def test_init_item_default():
    # test initializing a single item with all default values
    testItem = Item()
    assert len(testItem.uuid) == len(str(uuid4()))
    assert testItem.name == ""
    assert testItem.quantity == 0
    assert testItem.cost == 0
    assert testItem.weight == 0
    assert testItem.units == "each"
    assert testItem.datasheet == ""

def test_item_methods():
    testItem = itemFactory()
    assert testItem.printCost() == f"${testItem.cost*100:,.2f}/{testItem.units}"
    assert testItem.printName() == testItem.name.capitalize()
    assert testItem.printQuantity() == f"{testItem.quantity} {testItem.units}"

def test_init_many_items():
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

def test_increment_by_default():
    # test increasing quantity of item by default value of 1
    global indexItem
    item = items[indexItem]
    pre = item.quantity
    out = conn.incrementQuantity(item)
    assert out == 0
    assert conn.getItem(item.uuid).quantity == (pre + 1)
    indexItem += 1

def test_increment_by_value():
    # test increasing quantity of item by passed-in value
    global indexItem
    item = items[indexItem]
    pre = item.quantity 
    num = randint(maxsize/2)
    out = conn.incrementQuantity(item, num)
    assert out == 0
    assert conn.getItem(item.uuid).quantity == (pre + num)
    indexItem += 1

def test_increment_by_negative():
    # test trying to call incrementQuantity with a negative value for by
    global indexItem
    item = items[indexItem]
    num = -1*randint(maxsize)
    with warns(UserWarning, match = "You cannot increment by a non-positive value. Please use decrementQuantity"):
       out = conn.incrementQuantity(item, num)
    assert out == 1 
    indexItem += 1

def test_decrement_by_default():
    # test decreasing quantity of item by default value of 1
    global indexItem
    item = items[indexItem]
    pre = item.quantity
    out = conn.decrementQuantity(item)
    assert out == 0
    assert conn.getItem(item.uuid).quantity == (pre - 1)
    indexItem += 1

def test_decrement_by_value():
    # test decreasing quantity of item by passed-in value
    global indexItem
    item = items[indexItem]
    pre = item.quantity
    num = randint(pre)
    assert num <= pre
    out = conn.decrementQuantity(item, num)
    assert out == 0
    assert conn.getItem(item.uuid).quantity == (pre - num)
    indexItem += 1

def test_decrement_by_negative():
    # test trying to call decrementQuantity with a negative value for by
    global indexItem
    item = items[indexItem]
    num = -1*randint(maxsize)
    with warns(UserWarning, match = "You cannot decrement by a non-positive value. Please use incrementQuantity"):
       out = conn.decrementQuantity(item, num)
    assert out == 1 
    indexItem += 1

def test_destroy_item():
    # test deleting item from database
    global indexItem
    item = items[indexItem]
    out = conn.destroy(item)
    assert out == 0

    # test that item is really gone
    with warns(UserWarning, match = "No item with this UUID was found in the database."):
        out = conn.getItem(item.uuid)
    assert out == 1

def test_destroy_nonexistent_item():
    # test trying to delete an item that isn't in the database
    item = itemFactory()

    with warns(UserWarning, match = "No item with this UUID was found in the database."):
        out = conn.destroy(item)
    assert out == 1
