import os
import sys
import json
import pytest
import sqlite3
from numpy.random import randint
from uuid import uuid4
from Connection import Connection
from Item import Item

names_qry = "SELECT uuid, name FROM items;"

global nameslist
global unitslist
global conn
global items

path = os.getcwd() + '/inventory.sqlite'

conn = Connection(path)

with open("formatted_nouns.txt", mode = "r") as fp:
    nameslist = json.load(fp)

unitslist = ["meter", "gram", "yard", "mile", "kilogram", "foot", "second", "inch", "millimeter", "ohm", "farad", "volt", "amp", "each"]

def itemFactory(uuid = "") -> Item:
    idx1 = randint(len(nameslist))
    idx2 = randint(len(nameslist))

    name = nameslist[idx1] + " " + nameslist[idx2]
    quantity = randint(sys.maxsize)
    cost = randint(sys.maxsize)
    weight = randint(sys.maxsize)
    units = unitslist[randint(len(unitslist))]

    if uuid == "":
        return Item(name = name, quantity = quantity, cost = cost, weight = weight, units = units)
    else:
        return Item(uuid = uuid, name = name, quantity = quantity, cost = cost, weight = weight, units = units) 

items = [itemFactory(str(uuid4())) for i in range(1000)]
for k in range(len(items)):
        conn.create(items[k])

def test_init_item():
    # initialize a bunch of items with empty uuids and test their properties
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

def test_item_from_db():
    # initialize a bunch of items given uuids and test their properties
    for j in range(1000):
        testItem = conn.getItem(items[j].uuid)
        assert len(testItem.uuid) == len(str(uuid4()))
        assert testItem.quantity >= 0
        assert testItem.cost >= 0
        assert testItem.weight >= 0
        assert testItem.units in unitslist

def test_create_item():
    # test adding items to the database 
    # for k in range(len(items)):
    #    conn.create(items[k])
    pass

def test_increment():
    # test increasing quantity of item
    pass

def test_decrement():
    # test decreasing quantity of item
    pass

def test_delete_item():
    # test deleting item from database
    pass
