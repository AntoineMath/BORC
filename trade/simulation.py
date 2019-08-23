from random import randrange
import time


def __algo_simulation__():
    while True:
        yield randrange(3)
        time.sleep(60)


if __name__ == "__main__":
    for value in __algo_simulation__():
        print(value)
