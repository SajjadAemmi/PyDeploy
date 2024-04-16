import time
import random


def marriage(i):
    r = random.randint(0, 10)
    time.sleep(r)
    print(i)


def main():
    for child in ["mamad", "gholi", "goli", "alex"]:
        marriage(child)


if __name__ == "__main__":
    start_time = time.perf_counter()
    main()
    end_time = time.perf_counter()
    total_time = end_time - start_time
    print(f"Executed in {total_time:0.2f} seconds.")
