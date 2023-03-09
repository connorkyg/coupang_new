import time
import random


def sleep(num1, num2):
    return time.sleep(random.sample(range(num1, num2), 1)[0])
