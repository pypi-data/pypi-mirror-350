from decimal import Decimal as long
from fractions import Fraction as fraction
from functools import cache
from pyplus.tools.dec import dint, Calc

import math
import matplotlib
import matplotlib.pyplot as plt
import numba
import numpy as np
import numpy

from sympy import *

def safe_formula_solver(formula, **variables):
    allowed_symbols = {k: symbols(k) for k in variables.keys()}
    try:
        expr = sympify(formula, locals=allowed_symbols)
        return float(expr.subs(variables))
    except SympifyError:
        raise ValueError("Invalid formula")


def joseph_problem(n: int) -> int:
    """
    Joseph problem is a classic problem in computer science. It is a problem of finding the last person standing in a circle of people. The problem is named after the Greek mathematician Josephus. The problem can be solved using a simple algorithm called the Josephus problem. The algorithm works as follows:

    1. Start with a list of n people numbered from 1 to n.
    2. Start with a pointer to the first person in the list.
    3. Remove the person pointed to by the pointer.
    4. Move the pointer n-1 positions ahead in the list.
    5. Repeat steps 3 and 4 until there is only one person left in the list.
    6. The last person remaining in the list is the last person standing in the circle.

    The Josephus problem is a classic example of a mathematical problem that can be solved using a simple algorithm. The algorithm is simple and easy to understand, but it can be improved by using more advanced techniques such as dynamic programming or memoization.
    Args:
        n (int): The number of people in the circle.
    Returns:
        int: The number of the last person standing in the circle.
    """
    if n == 1:
        return 1
    else:
        return (joseph_problem(n - 1) + n - 1) % n + 1

@cache
def fib(n):
    if n == 0:
        return 0
    elif n == 1:
        return 1
    else:
        return fib(n-1) + fib(n-2)
    
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

def is_palindrome(n):
    return str(n) == str(n)[::-1]

def is_even(n):
    return n % 2 == 0

def is_odd(n):
        return n % 2 == 1

def c(n, r):
    return math.factorial(n) // (math.factorial(r) * math.factorial(n-r))

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def hcf(a, b):
    return math.gcd(a, b)

def prime_factors(n):
    factors = []
    d = 2
    while d*d <= n:
        while (n % d) == 0:
            factors.append(d)
            n //= d
        d += 1
    if n > 1:
        factors.append(n)
    return factors

def prime_divisors(n):
    factors = prime_factors(n)
    divisors = []
    for factor in factors:
        divisors.append(c(n, factor))
    return divisors

def p(n, r):
    return c(n, r) // math.factorial(r)