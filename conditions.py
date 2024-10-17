def add(a,b):
    return a+b

def test_add():
    assert add(2,3) == 5
    assert add(5,10) == 15

def divide(a,b):
    if b == 0:
        raise ValueError("Cannot divide by 0")
    return a/b
    

test_add()

divide(4,0)

