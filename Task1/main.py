from bloom_filter import BloomFilter
def check_password_uniqueness(filter: BloomFilter, passwords: list[str]) -> dict[str, bool]:
    return {password:filter.contains(password) for password in passwords}

if __name__ == "__main__":
    # Ініціалізація фільтра Блума
    bloom = BloomFilter(hash_functions_count=4)

    [bloom.add(password) for password in ["password123", "admin123", "qwerty123"]]


    new_passwords_to_check = ["password123", "newpassword", "admin123", "guest"]
    results = check_password_uniqueness(bloom, new_passwords_to_check)

    # Виведення результатів
    for password, status in results.items():
        print(f"Пароль '{password}' - {'вже використаний' if status else 'унікальний'}.")
