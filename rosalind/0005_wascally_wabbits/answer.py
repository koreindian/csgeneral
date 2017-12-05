def rabbit_fib(n, k):
    n1 = n2 = 1

    for _ in range(n - 2):
        n1, n2 = n2, k * n1 + n2

    return n2

print(rabbit_fib(5, 3))
print(rabbit_fib(28, 2))
