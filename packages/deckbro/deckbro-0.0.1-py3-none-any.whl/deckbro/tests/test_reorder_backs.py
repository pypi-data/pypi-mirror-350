from deckbro.render import reorder_backs
import pytest


def test_reorder_2cols_nofill():

    backs = ["1", "2", "3", "4", "5", "6"]

    rbacks = reorder_backs(backs, 2)

    assert rbacks == ["2", "1", "4", "3", "6", "5"]

def test_reorder_3cols_nofill():

    backs = ["1", "2", "3", "4", "5", "6"]

    rbacks = reorder_backs(backs, 3)

    assert rbacks == ["3", '2', '1', "6", "5", "4"]

def test_reorder_2cols_fill():

    backs = ["1", "2", "3", "4", "5"]

    rbacks = reorder_backs(backs, 2)

    assert rbacks == ["2", "1", "4", "3", None, "5"]

def test_reorder_3cols_fill_1():

    backs = ["1", "2", "3", "4", "5"]

    rbacks = reorder_backs(backs, 3)

    assert rbacks == ["3", "2", "1", None, "5", "4"]

def test_reorder_3cols_fill_2():

    backs = ["1", "2", "3", "4"]

    rbacks = reorder_backs(backs, 3)

    assert rbacks == ["3", "2", "1", None, None, "4"]