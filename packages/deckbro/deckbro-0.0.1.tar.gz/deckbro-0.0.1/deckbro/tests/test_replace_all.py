import pytest 
from deckbro.svg import replace_all

def test_replace_all():

    r = replace_all(
        "banana bag",
        {
            "ba":"E",
            "bana" : "D",
            "a" : "F",
            "g" : "T"
        }
    )

    assert r == "DnF ET"

def test_replace_all_no_match():
    r = replace_all(
        "banana bag",
        {
            "E": "ba",
            "A" : "X",
            "Z" : "T"
        }
    )
    
    assert r == "banana bag"

def test_replace_all_targets_not_matched():
    r = replace_all(
        "banana bag",
        {
            "ba" : "E",
            "E" : "Z"
        }
    )

    assert r == "Enana Eg"
