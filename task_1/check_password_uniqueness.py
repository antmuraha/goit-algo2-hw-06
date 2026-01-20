from task_1.bloom_filter import BloomFilter


NOT_VALID = "non valid"
ALREADY_USED = "already used"
UNIQUE = "unique"


def check_password_uniqueness(
    bloom_filter: BloomFilter, passwords: list
) -> dict[str, str]:
    results = {}
    for password in passwords:
        if not isinstance(password, str) or password == "":
            results[password] = NOT_VALID
        elif bloom_filter.check(password):
            results[password] = ALREADY_USED
        else:
            results[password] = UNIQUE
    return results


# Example usage
if __name__ == "__main__":
    # Initialize Bloom filter
    bloom = BloomFilter(size=1000, num_hashes=3)

    # Adding existing passwords
    existing_passwords = ["password123", "admin123", "qwerty123"]
    for password in existing_passwords:
        bloom.add(password)

    print("Bloom filter initialized.", bloom, "\n")

    # Checking new passwords
    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Displaying results
    for password, status in results.items():
        print(f"Password '{password}' - {status}.")
