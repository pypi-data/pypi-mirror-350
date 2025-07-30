import pytest
from deckbro.svg import find_first_of

def test_find_first_of_not_found():
    r = find_first_of("banana bag", ["bane", "bagger"])
    assert r[0] == len("banana bag")
    assert r[1] == ""

def test_find_first_of_no_collision():
    r = find_first_of("banana bag", ["ban", "bagger"])
    assert r[0] == 0
    assert r[1] == "ban"

def test_find_first_of_collision_by_index_no_overlap():
    r = find_first_of("banana bag", ["anana", "bag"])
    assert r[0] == 1
    assert r[1] == "anana"

def test_find_first_of_collision_by_index_overlap():
    r = find_first_of("banana bag", ["ana", "bagger"])
    assert r[0] == 1
    assert r[1] == "ana"

def test_find_first_of_collision_by_index_overlap_2():
    r = find_first_of("banana bag", ["ana", "nana"])
    assert r[0] == 1
    assert r[1] == "ana"

def test_find_first_of_collision_by_length():
    r = find_first_of("banana bag", ["bana", "banana"])
    assert r[0] == 0
    assert r[1] == "banana"

    