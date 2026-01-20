# GoIT Algorithms 2.0 Homework

This repository contains solutions for two algorithmic problems:

- Password uniqueness checks using Bloom Filter - for working with big data where memory conservation and processing speed are critical.

- Counting unique elements in large data sets, including exact methods and approximate algorithms such as HyperLogLog.

## Task 1. Checking the uniqueness of passwords using the Bloom filter

The check_password_uniqueness() function checks the uniqueness of passwords using a Bloom filter. This function determines whether a password has been used before, without having to store the passwords themselves.

**Run the script:**

```bash
python task_1/check_password_uniqueness.py
```

**Output:**

```
Bloom filter initialized. BloomFilter:
        bits: 1000
        number hashes: 3
        bloom length (8 bits): 125
        number bits set: 9
        estimated elements added: 3
        current false positive rate: 0.000001

Password 'password123' - already used.
Password 'newpassword' - unique.
Password 'admin123' - already used.
Password 'guest' - unique.
```

## Task 2. HyperLogLog performance comparison with accurate unique element counting
