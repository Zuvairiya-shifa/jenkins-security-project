from app import calculate, greet

def test_calculate():
    assert calculate(5, 3) == 8

def test_greet():
    assert greet("Student") == "Hello Student"