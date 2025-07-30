from deckbro.render import interleave_front_back

def test_interleave_front_back_nopad():

    flist = ["1", "2", "3", "4", "5", "6", "7", "8"]
    blist = ["a", "b", "c", "d", "e", "f", "g", "h"]

    rlist = interleave_front_back(flist, blist, 4)

    assert rlist == [
        "1", "2", "3", "4",
        "a", "b", "c", "d",
        "5", "6", "7", "8",
        "e", "f", "g", "h"
    ]


def test_interleave_front_back_same_padding():
    
    flist = ["1", "2", "3", "4", "5", "6", "7", "8"]
    blist = ["a", "b", "c", "d", "e", "f", "g", "h"]

    rlist = interleave_front_back(flist, blist, 3)

    print("rlist", rlist)

    assert rlist == [
        "1", "2", "3",
        "a", "b", "c",
        "4", "5", "6",
        "d", "e", "f",
        "7", "8", None,
        "g", "h", None
    ]

def test_interleave_front_back_diff_padding():

    flist = ["1", "2", "3", "4", "5", "6", "7"]
    blist = ["a", "b", "c", "d", "e", "f", "g", "h"]

    rlist = interleave_front_back(flist, blist, 3)

    assert rlist == [
        "1", "2", "3",
        "a", "b", "c",
        "4", "5", "6",
        "d", "e", "f",
        "7", None, None,
        "g", "h", None
    ]