import json
import os
from typing import Generator

from datasketch import HyperLogLog


def read_logs():
    if not os.path.exists("putLogHere/lms-stage-access.log"):
        raise FileNotFoundError(
            "Log file not found. Please ensure the file exists."
        )
    with open("putLogHere/lms-stage-access.log", "r", encoding='utf-8') as file:
        for log in file:
            yield json.loads(log)["remote_addr"]


generator = read_logs


def count_unique() -> int:
    addresses = set()
    for address in generator():
        addresses.add(address)
    return len(addresses)


def estimate_unique() -> float:
    hll = HyperLogLog(p=16)
    for address in generator():
        hll.update(address.encode("utf-8"))
    return hll.count()


def measure_time(func):
    import time

    start = time.time()
    result = func()
    end = time.time()
    return result, end - start


def generate_random_ip_addresses() -> Generator[str, None, None]:
    import random

    count = 100000

    yield from [
        f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
        for _ in range(count)
    ]


def run() -> None:
    exact_count, exact_time = measure_time(count_unique)
    hll_count, hll_time = measure_time(estimate_unique)

    print(f"{'':<25} | {'Точний підрахунок':<20} | {'HyperLogLog':<20}")
    print("-" * 70)
    print(f"{'Унікальні елементи':<25} | {exact_count:<20} | {hll_count:<20}")
    print(f"{'Час виконання (сек.)':<25} | {exact_time:<20.6f} | {hll_time:<20.6f}")


if __name__ == "__main__":
    run()

    print("\n")

    generator = generate_random_ip_addresses
    print("random addresses: 100000")
    run()
