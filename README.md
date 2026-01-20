# GoIT Algorithms 2.0 Homework

This repository contains solutions for two algorithmic problems:

- Password uniqueness checks using Bloom Filter - for working with big data where memory efficiency and processing speed are critical.

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

Comparison of accurate counting of unique elements using the `set` structure and counting using `HyperLogLog`.

```bash

# precision = 4
python task_2/count_unique_ips.py "https://drive.usercontent.google.com/u/0/uc?id=13NUCSG7l_z2B7gYuQubYIpIjJTnwOAOb&export=download" --precision 4

# Reading log from URL...

# ==================================================
# Exact counting using set:
# ==================================================
# Using cached file: .cache/4620c394dff8a4d40332f5c93f30f758.log
# Unique IP addresses (exact): 28

# ==================================================
# Approximate counting using HyperLogLog (precision=4):
# ==================================================
# Using cached file: .cache/4620c394dff8a4d40332f5c93f30f758.log
# Unique IP addresses (HyperLogLog): 26

# ==================================================
# Comparison:
# ==================================================
# Exact count:        28
# HyperLogLog count:  26
# Absolute error:     2
# Error rate:         7.14%

# Memory usage (estimated):
# Set:                ~1,792 bytes
# HyperLogLog:        ~16 bytes
# Memory reduction:   112.0x
# Using cached file: .cache/4620c394dff8a4d40332f5c93f30f758.log
# Using cached file: .cache/4620c394dff8a4d40332f5c93f30f758.log
# Set method: 28 unique IPs in 0.333126 seconds
# HyperLogLog method: 26 unique IPs in 0.526195 seconds


# precision = 6
python task_2/count_unique_ips.py "https://drive.usercontent.google.com/u/0/uc?id=13NUCSG7l_z2B7gYuQubYIpIjJTnwOAOb&export=download" --precision 8

# Reading log from URL...

# ==================================================
# Exact counting using set:
# ==================================================
# Using cached file: .cache/4620c394dff8a4d40332f5c93f30f758.log
# Unique IP addresses (exact): 28

# ==================================================
# Approximate counting using HyperLogLog (precision=8):
# ==================================================
# Using cached file: .cache/4620c394dff8a4d40332f5c93f30f758.log
# Unique IP addresses (HyperLogLog): 28

# ==================================================
# Comparison:
# ==================================================
# Exact count:        28
# HyperLogLog count:  28
# Absolute error:     0
# Error rate:         0.00%

# Memory usage (estimated):
# Set:                ~1,792 bytes
# HyperLogLog:        ~256 bytes
# Memory reduction:   7.0x
# Using cached file: .cache/4620c394dff8a4d40332f5c93f30f758.log
# Using cached file: .cache/4620c394dff8a4d40332f5c93f30f758.log
# Set method: 28 unique IPs in 0.330612 seconds
# HyperLogLog method: 28 unique IPs in 0.407142 seconds

```

### Development

```bash
# Run local development on the small example structure data
python task_2/count_unique_ips.py data/example-access-data.log

# Reading log from local file...
# ==================================================
# Exact counting using set:
# ==================================================
# Unique IP addresses (exact): 2

# ==================================================
# Approximate counting using HyperLogLog (precision=5):
# ==================================================
# Unique IP addresses (HyperLogLog): 2

# ==================================================
# Comparison:
# ==================================================
# Exact count:        2
# HyperLogLog count:  2
# Absolute error:     0
# Error rate:         0.00%

# Memory usage (estimated):
# Set:                ~128 bytes
# HyperLogLog:        ~32 bytes
# Memory reduction:   4.0x
```

## 🤝 Contributing

This is a repo for the GoIT course. If you're also a student working on similar exercises, feel free to use this as a reference, but make sure to understand the concepts and implement your own solution.

## 📄 License

This project is created for educational purposes as part of the GoIT course curriculum.
