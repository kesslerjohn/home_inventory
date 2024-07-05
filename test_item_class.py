from os import remove, listdir, getcwd
from pytest import warns
from uuid import uuid4
from Connection import Connection
from Item import Item
from utils import itemFactory, nameslist, unitslist
import pytest

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
    assert testItem.printCost() == f"${testItem.cost/100:,.2f}/{testItem.units}"
    assert testItem.printName() == testItem.name.capitalize()
    assert testItem.printQuantity() == f"{testItem.quantity} {testItem.units}"

def test_init_many_items():
    # initialize a bunch of items with empty uuids and test their properties
    # this is really testing itemFactory() as much as anything
    ids = []
    for i in range(100):
        testItem = itemFactory()
        assert len(testItem.uuid) == len(str(uuid4()))
        assert testItem.quantity >= 0
        assert testItem.cost >= 0
        assert testItem.weight >= 0
        assert testItem.units in unitslist
        ids.append(testItem.uuid)
    assert len(set(ids)) == len(ids)
