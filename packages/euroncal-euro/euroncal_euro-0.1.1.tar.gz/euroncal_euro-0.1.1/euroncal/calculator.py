def add(a,b):
    """this will return addition of two number """
    return a+b

def subtract(a,b):
    return a-b


def multiply(a,b):
    return a*b


def divide(a,b):
    if b == 0 :
        raise ValueError("cant divide by zero")
    return a/b

def power(a,b):
    return a**b

