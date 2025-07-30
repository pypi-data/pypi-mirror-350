import math
a=math.pi
def add(x,y):
    return x+y
def subtract(x,y):
    return x-y
def multiply(x,y):
    return x*y
def divide(x,y):
    return x/y
def absolute_value(x):
    n=str(x)
    n=list(n)
    if n[0] == '-':
        n.pop(0)
    n = ''.join(n)
    n = int(n)
    return n
def exponentiation(x,y):
    n=x
    for i in range(y):
        x=x*n
    return x
def CEIL(x):
    n=math.ceil(x)
    return n
def FLOOR(x):
    n=math.floor(x)
    return n
def circle(x):
    n = x*x*a
    return n
def square(x,y):
    return x*y
def nth_root(num, n, epsilon=1e-10):
    if num < 0 and n % 2 == 0:
        raise ValueError("负数没有实数偶次方根")
    guess = num
    while abs(guess ** n - num) > epsilon:
        guess = ((n - 1) * guess + num / (guess ** (n - 1))) / n
    return guess
def SIN(x):
    n = math.sin(x)
    return n
def COS(x):
    n = math.cos(x)
    return n
def TAN(x):
    n = math.tan(x)
    return n
