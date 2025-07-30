import math

def superfactorial(n):
    prod = 1
    for i in range(1,n+1):
        prod *= math.factorial(i)
    print(prod)

    