import mmh3


class BloomFilter:
    def __init__(self, hash_functions_count: int = 8) -> None:
        self.hash_functions_count = hash_functions_count
        self.bit_array = [0] * hash_functions_count ** 2

    def add(self, item: str) -> None:
        for i in range(self.hash_functions_count):
            index = mmh3.hash(item, i) % len(self.bit_array)
            self.bit_array[index] = 1

    def contains(self, item: str) -> bool:
        for i in range(self.hash_functions_count):
            index = mmh3.hash(item, i) % len(self.bit_array)
            if self.bit_array[index] == 0:
                return False
        return True
