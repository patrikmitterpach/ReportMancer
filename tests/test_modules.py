from source.moduleA import add

def test_add():
    assert(add(1,2)  == 3)
    assert(add(1,3)  == 4)
    assert(add(-1,5) == 4)
