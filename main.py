'''
give me a python3 code that does this.

1. Get any product that can be found in Coupang.
2. Write an article about the product in Korean. (review, description, issues, price, manual or something. It would be better to be long as much as you can give me.)
3. Save the article to file. File name should be in form "{Product_name}_{nowdate}"
4. Post the article to Tistory blog using Tistory api. Posting every 30 to 60 minutes. (Interval time should be random).
'''

# make an article using gpt
# save the article in db

# post on blog from db


# -*- coding: utf-8 -*-

import time
from data import form
from data.keywords import keyword
from apis import coupang
from apis import tistory
from lib import sleep

input("check the account for tistory. ok?: ")


def auto_A_type():
    # COMMENT: random keyword 검색 결과를 tistory에 form에 맞추어 posting
    for i in range(10):  # COMMENT: 시간당 최대 10번이므로 10으로 설정이 default
        product_data = coupang.search_product()
        sleep(2, 4)
        content = form.top_ten(product_data, keyword)
        sleep(2, 4)
        tistory.tistory().post_write(keyword, content)  # COMMENT: Tistory에 API 글쓰기가 많아지면 차단됨. Selenium으로 대체
        sleep(30, 600)
    time.sleep(60 * 60)  # COMMENT: (60*65)초 interval
    return 0


def auto_B_type():
    pass


if __name__ == '__main__':
    pass
