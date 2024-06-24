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
global path

path = os.getcwd() + '/inventory.sqlite'

con = Connection(path)
con.cursor().execute(names_qry).fetchall()

pliers = con.getItem('0a6e74b1-f5cf-4579-8bf9-d103b6032c95')

pliers.name
pliers.uuid
pliers.quantity

with open("formatted_nouns.txt", mode = "r") as fp:
    nameslist = json.load(fp)

unitslist = ["meter", "gram", "yard", "mile", "kilogram", "foot", "second", "inch", "millimeter", "ohm", "farad", "volt", "amp"]

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
    ids = [str(uuid4()) for i in range(1000)]
    for j in range(1000):
        testItem = itemFactory(ids[j])
        assert len(testItem.uuid) == len(str(uuid4()))
        assert testItem.quantity >= 0
        assert testItem.cost >= 0
        assert testItem.weight >= 0
        assert testItem.units in unitslist
        assert testItem.uuid in ids

def test_connection():
    # should accept a valid connection
    con = Connection(path)
    pass

def test_create_item():
    # test adding items to the database
    con = Connection(path)
    pass

def test_increment():
    pass

def test_decrement():
    pass
