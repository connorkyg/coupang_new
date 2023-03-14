import time
import random
from data import keywords

rnd = 3
kwrd = [[] for _ in range(rnd)]
for i in range(rnd):
    kwrd[i] = random.choice(keywords.keyword_list)
    print(kwrd[i])
    time.sleep(1)