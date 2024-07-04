from os import remove, listdir, getcwd, mkdir, rmdir, chdir, remove
from glob import glob
from sys import maxsize
from json import load
from pytest import warns
from numpy.random import randint
from uuid import uuid4
from Connection import Connection
from Item import Item
from utils import itemFactory, nameslist, unitslist
import pytest

global conn
global indexItem
indexItem = 0

test_path = getcwd() + '/test_inventory.sqlite'

items = [itemFactory(str(uuid4())) for i in range(1000)]

def test_init_db():
    # test that a warning is raised when connecting to a db file not in the cwd.
    if ('test_inventory.sqlite') in listdir():
        remove('test_inventory.sqlite')

    global conn
    with warns(UserWarning, match = "A SQLite DB named test_inventory.sqlite was not found"):
        conn = Connection(test_path)

def test_create_item():
    res = []
    cdir = getcwd()
    if "qr_tests" not in listdir():
        mkdir("qr_tests")
    chdir("qr_tests")
    for k in range(len(items)):
        res.append(conn.create(items[k]))
    # check that all creations worked
    assert all([i == 0 for i in res])

    # clean up
    for f in glob("*.png"):
        remove(f)

    chdir(cdir)

    rmdir("qr_tests")

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

def test_search_connection():
    # test whether searching returns objects with similar names
    global nameslist
    noun = nameslist[randint(len(nameslist))]
    names = [nameslist[randint(len(nameslist))] + " " + noun for i in range(10)]
    names += [noun + " " + nameslist[randint(len(nameslist))] for i in range(10)]
    names += [nameslist[randint(len(nameslist))] + " " + noun + " " + nameslist[randint(len(nameslist))] for i in range(10)]
    cdir = getcwd()
    if "search_tests" not in listdir():
        mkdir("search_tests")
    chdir("search_tests")
    for name in names:
        conn.create(itemFactory(name = name))
    out = conn.search(noun)
    assert len(out) >= 30

    # clean up
    for f in glob("*.png"):
        remove(f)

    chdir(cdir)

    rmdir("search_tests")

def test_search_no_results():
    name = str(randint(1000, 10000))
    out = conn.search(name)
    assert len(out) == 0

def test_search_empty_string():
    out = conn.search("")
    assert len(out) == 0

@pytest.mark.xfail
def test_execute_query():
    # test whether execute_query() really does its job
    # TODO: decide whether this method needs to exist or should be replaced by 
    #       methods for specific actions
    assert False
