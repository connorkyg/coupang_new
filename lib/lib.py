import html
import time
import random


def random_sleep(num1, num2):
    return time.sleep(random.sample(range(num1, num2), 1)[0])


def convert_to_html(data):
    return html.escape(data).replace("\n", "<br />")


def now():
    return time.strftime('%Y%m%d_%H%M%S')