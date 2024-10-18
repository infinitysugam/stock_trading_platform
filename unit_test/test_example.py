def add(a,b):
    return a+b

def test_add():
    assert add(2,3) == 5
    assert add(10,5) == 15
    assert add(-1,1) == 0