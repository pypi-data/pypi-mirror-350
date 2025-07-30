def factorial(x):
    result = 1
    for i in range(2, x + 1):
        result *= i
    return result

def superfactorial(n):
    prod = 1
    for i in range(1, n + 1):
        prod *= factorial(i)
    print(prod)
