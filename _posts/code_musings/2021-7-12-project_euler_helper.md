---
layout: post
title: Project Euler helper methods
permalink: code_musings/project_euler_helpers
---
Project Euler has a number of interesting maths problems that they want us to solve using code.

Many of the problems centre around prime factorisation. Below is a handy helper method in Python to get the prime factors of an integer `n` - 


```python
def get_prime_factorisation(n: int) -> dict:
    out = {}
    if n % 2 == 0:
        cnt = 0
        while n % 2 == 0:
            cnt += 1
            n /= 2
        out[2] = cnt

    for i in range(3, int(sqrt(n) + 2), 2):
        if n % i == 0:
            cnt = 0
            while n % i == 0:
                cnt += 1
                n = n // i
            out[i] = cnt
    if n > 2:
        out[n] = 1
    return out


if __name__ == "__main__":
    n = input("Enter integer: ")
    print(get_prime_factorisation(int(n)))
```

The output of `get_prime_factorisation` would be a dictionary, where the keys are the prime factors, and the values are the exponents of the prime factors. Examples - 

1. `n = 42`  => `{2: 1, 3: 1, 7: 1}`, since $$ 42 = 7 \times 3 \times 2 $$
2. `n = 27` => `{3: 3}`, since $$ 27 = 3^3 $$
3. `n = 59` => `{59: 1}`, since 59 is prime.